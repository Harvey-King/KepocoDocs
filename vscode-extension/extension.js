'use strict';
const vscode = require('vscode');
const fs = require('node:fs/promises');
const path = require('node:path');
const {settingsPlan} = require('./setup');

async function folderForCommand() {
    const folders = vscode.workspace.workspaceFolders || [];
    if (!folders.length) throw new Error('Open your game folder with File > Open Folder first.');
    if (folders.length === 1) return folders[0];
    return vscode.window.showWorkspaceFolderPick();
}

async function copyTree(source, target) {
    await fs.mkdir(target, {recursive: true});
    let count = 0;
    for (const entry of await fs.readdir(source, {withFileTypes: true})) {
        const src = path.join(source, entry.name);
        const dst = path.join(target, entry.name);
        if (entry.isDirectory()) count += await copyTree(src, dst);
        else if (entry.isFile()) {
            await fs.copyFile(src, dst);
            if ((await fs.stat(src)).size !== (await fs.stat(dst)).size) throw new Error('Copy verification failed: ' + dst);
            count++;
        }
    }
    return count;
}

async function setupProject(context) {
    const folder = await folderForCommand();
    if (!folder) return;
    const approval = await vscode.window.showWarningMessage(
        'Add Kepoco editor hints to ' + folder.name + '? Existing Kepoco stubs in typings will be replaced; unrelated files stay untouched. No firmware or game code is executed.',
        {modal: true}, 'Set Up Project');
    if (approval !== 'Set Up Project') return {cancelled: true};
    const assetRoot = path.join(context.extensionPath, 'assets');
    let count = await copyTree(path.join(assetRoot, 'typings'), path.join(folder.uri.fsPath, 'typings'));
    count += await copyTree(path.join(assetRoot, 'vendor', 'micropython'), path.join(folder.uri.fsPath, 'vendor', 'micropython'));
    const config = vscode.workspace.getConfiguration('python.analysis', folder.uri);
    const plan = settingsPlan({extraPaths: config.get('extraPaths'), typeCheckingMode: config.get('typeCheckingMode'), diagnosticSeverityOverrides: config.get('diagnosticSeverityOverrides')});
    for (const [key, value] of Object.entries(plan)) {
        await config.update(key, value, vscode.ConfigurationTarget.WorkspaceFolder);
    }
    const resolved = vscode.workspace.getConfiguration('python.analysis', folder.uri);
    if (resolved.get('stubPath') !== './typings') throw new Error('Workspace settings did not retain the requested stub path.');
    await vscode.window.showInformationMessage('Kepoco hints installed (' + count + ' files). Try typing kepoco.display. or run Kepoco: Check IntelliSense.');
    return {filesCopied: count, folder: folder.uri.fsPath};
}

function hoverText(hovers) {
    return (hovers || []).flatMap(h => h.contents.map(c => typeof c === 'string' ? c : c.value || '')).join('\n');
}

async function verifyIntelliSense(context, options = {}) {
    const folder = await folderForCommand();
    if (!folder) return;
    const file = vscode.Uri.joinPath(folder.uri, 'examples', 'kepoco-intellisense-check.py');
    await fs.mkdir(path.dirname(file.fsPath), {recursive: true});
    const lines = [
        '# Editor verification fixture; not executable desktop/emulator code.',
        'import kepoco', 'import time',
        'kepoco.display.fill(0)', 'kepoco.buttonA.pressed()',
        'kepoco.audio.stop()', 'kepoco.saveData.getName()', 'kepoco.link.receive()',
        'sprite = kepoco.Sprite(8, 8, bytearray(8))', 'sprite.setFrame(0)',
        'time.sleep(0)',
        'kepoco.display.drawFilledRectangle(1, 2, 3, 4, 1)',
        'kepoco.display.getPixel(0, 0)'
    ];
    await fs.writeFile(file.fsPath, lines.join('\n') + '\n', 'utf8');
    const document = await vscode.workspace.openTextDocument(file);
    await vscode.window.showTextDocument(document, {preview: true, preserveFocus: true});
    const requirements = [
        {prefix: 'kepoco.display.', expected: ['fill','drawText','drawFilledRectangle','drawLine','drawEllispe','getPixel','width','height','WHITE','DARKGRAY']},
        {prefix: 'kepoco.buttonA.', expected: ['pressed','justPressed','update']},
        {prefix: 'kepoco.audio.', expected: ['play','playBlocking','stop','setEnabled']},
        {prefix: 'kepoco.saveData.', expected: ['setName','setItem','getItem','hasItem','save']},
        {prefix: 'kepoco.link.', expected: ['send','receive','init']},
        {prefix: 'sprite.', expected: ['setFrame','getFrame','x','y','width','height']},
        {prefix: 'time.', expected: ['ticks_ms','ticks_diff','ticks_add','sleep_ms']}
    ];
    const completionChecks = [];
    const errors = [];
    // Retry the provider only while it is initializing, with a fixed upper bound.
    for (const requirement of requirements) {
        const line = lines.findIndex(s => s.startsWith(requirement.prefix));
        let labels = [];
        let lastError = '';
        for (let attempt = 0; attempt < (options.maxAttempts || 45); attempt++) {
            try {
                const completion = await vscode.commands.executeCommand('vscode.executeCompletionItemProvider', document.uri, new vscode.Position(line, requirement.prefix.length), '.');
                labels = (completion && completion.items || []).map(i => typeof i.label === 'string' ? i.label : i.label.label);
                if (requirement.expected.every(name => labels.includes(name))) break;
            } catch (error) { lastError = String(error); }
            await new Promise(resolve => setTimeout(resolve, 400));
        }
        const missing = requirement.expected.filter(name => !labels.includes(name));
        completionChecks.push({prefix: requirement.prefix, expected: requirement.expected, labels, missing, passed: missing.length === 0, providerError: lastError});
    }
    const hoverLine = lines.findIndex(s => s.includes('drawFilledRectangle('));
    const hoverColumn = lines[hoverLine].indexOf('drawFilledRectangle') + 3;
    const hovers = await vscode.commands.executeCommand('vscode.executeHoverProvider', document.uri, new vscode.Position(hoverLine, hoverColumn));
    const hover = hoverText(hovers);
    const hoverPassed = hover.includes('drawFilledRectangle') && hover.includes('thumbyGraphics.py:108');
    const signatureColumn = lines[hoverLine].indexOf('(') + 1;
    const signature = await vscode.commands.executeCommand('vscode.executeSignatureHelpProvider', document.uri, new vscode.Position(hoverLine, signatureColumn), '(');
    const signatureLabels = (signature && signature.signatures || []).map(s => s.label);
    const signaturePassed = signatureLabels.some(s => s.includes('width') && s.includes('height') && s.includes('colour'));
    const getPixelLine = lines.findIndex(s => s.includes('getPixel('));
    const getPixelHovers = await vscode.commands.executeCommand('vscode.executeHoverProvider', document.uri, new vscode.Position(getPixelLine, lines[getPixelLine].indexOf('getPixel') + 2));
    const getPixelHover = hoverText(getPixelHovers);
    const warningPassed = getPixelHover.includes('does not return') && getPixelHover.includes('None');
    const definitions = await vscode.commands.executeCommand('vscode.executeDefinitionProvider', document.uri, new vscode.Position(hoverLine, hoverColumn));
    const definitionFiles = (definitions || []).map(d => (d.uri || d.targetUri).fsPath);
    const definitionPassed = definitionFiles.some(p => p.includes('typings') && p.includes('thumbyGraphics'));
    const diagnostics = vscode.languages.getDiagnostics(document.uri).map(d => ({message: d.message, severity: d.severity, code: d.code}));
    for (const d of diagnostics) if (d.severity === vscode.DiagnosticSeverity.Error) errors.push(d.message);
    const result = {scope: 'Real VS Code language-provider calls; no hardware execution.', folder: folder.uri.fsPath,
        completionChecks, hoverPassed, hover, signaturePassed, signatureLabels, warningPassed, getPixelHover,
        definitionPassed, definitionFiles, diagnostics,
        passed: completionChecks.every(c => c.passed) && hoverPassed && signaturePassed && warningPassed && definitionPassed && errors.length === 0};
    const report = vscode.Uri.joinPath(folder.uri, '.vscode', 'kepoco-intellisense-report.json');
    await fs.mkdir(path.dirname(report.fsPath), {recursive: true});
    await fs.writeFile(report.fsPath, JSON.stringify(result, null, 2), 'utf8');
    if (!options.silent) {
        const message = result.passed ? 'Kepoco IntelliSense checks passed: completions, hover docs, signatures and definitions.' : 'Kepoco IntelliSense check failed. Open the report for details; check workspace trust, Python/Pylance and typings settings.';
        const choice = await vscode.window.showInformationMessage(message, 'Open Report');
        if (choice === 'Open Report') await vscode.window.showTextDocument(await vscode.workspace.openTextDocument(report));
    }
    return result;
}

function activate(context) {
    const openDoc = async name => vscode.commands.executeCommand('markdown.showPreview', vscode.Uri.file(path.join(context.extensionPath, 'assets', 'docs', name)));
    const handlers = {
        'kepoco.openGettingStarted': () => openDoc('GETTING_STARTED.md'),
        'kepoco.openApiReference': () => openDoc('API_REFERENCE.md'),
        'kepoco.openFirmwareNotes': () => openDoc('FIRMWARE_NOTES.md'),
        'kepoco.setupProject': () => setupProject(context),
        'kepoco.verifyIntelliSense': () => verifyIntelliSense(context)
    };
    for (const [name, handler] of Object.entries(handlers)) {
        context.subscriptions.push(vscode.commands.registerCommand(name, async () => {
            try { return await handler(); }
            catch (error) { await vscode.window.showErrorMessage('Kepoco: ' + String(error)); throw error; }
        }));
    }
    return {verifyIntelliSense: options => verifyIntelliSense(context, options), setupProject: () => setupProject(context)};
}

module.exports = {activate, deactivate() {}};
