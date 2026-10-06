const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const root = path.join(__dirname, '..', 'vscode-extension');

test('extension provides documentation, setup and validation commands', () => {
    const manifestPath = path.join(root, 'package.json');
    assert.ok(fs.existsSync(manifestPath), 'The installable VS Code extension is missing');
    const pkg = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
    const commands = new Set(pkg.contributes.commands.map(c => c.command));
    for (const name of ['kepoco.openGettingStarted', 'kepoco.openApiReference', 'kepoco.openFirmwareNotes', 'kepoco.setupProject', 'kepoco.verifyIntelliSense']) {
        assert.ok(commands.has(name), `Missing command ${name}`);
    }
    assert.ok(pkg.extensionDependencies.includes('ms-python.vscode-pylance'));
    assert.ok(pkg.contributes.snippets.some(s => s.language === 'python'));
});

test('project setup preserves unrelated settings and existing type paths', () => {
    const modulePath = path.join(root, 'setup.js');
    assert.ok(fs.existsSync(modulePath), 'Project setup implementation is missing');
    const {settingsPlan} = require(modulePath);
    const plan = settingsPlan({
        extraPaths: ['./my-lib'],
        diagnosticSeverityOverrides: {reportUnusedImport: 'warning'},
        typeCheckingMode: 'strict'
    });
    assert.deepEqual(plan.extraPaths, ['./my-lib', './vendor/micropython']);
    assert.equal(plan.stubPath, './typings');
    assert.equal(plan.typeCheckingMode, 'strict');
    assert.equal(plan.diagnosticSeverityOverrides.reportUnusedImport, 'warning');
    assert.equal(plan.diagnosticSeverityOverrides.reportMissingModuleSource, 'none');
    assert.notEqual(plan.diagnosticSeverityOverrides.reportUndefinedVariable, 'none');
    assert.notEqual(plan.diagnosticSeverityOverrides.reportMissingImports, 'none');
});

test('verification creates its report in a clean workspace without .vscode', async () => {
    const cache = path.join(__dirname, '..', '.cache');
    fs.mkdirSync(cache, {recursive: true});
    const workspace = fs.mkdtempSync(path.join(cache, 'intellisense-clean-'));
    const entry = path.join(root, 'extension.js');
    const Module = require('node:module');
    const originalLoad = Module._load;
    const previousModule = require.cache[entry];
    const completions = {
        'kepoco.display.': ['fill', 'drawText', 'drawFilledRectangle', 'drawLine', 'drawEllispe', 'getPixel', 'width', 'height', 'WHITE', 'DARKGRAY'],
        'kepoco.buttonA.': ['pressed', 'justPressed', 'update'],
        'kepoco.audio.': ['play', 'playBlocking', 'stop', 'setEnabled'],
        'kepoco.saveData.': ['setName', 'setItem', 'getItem', 'hasItem', 'save'],
        'kepoco.link.': ['send', 'receive', 'init'],
        'sprite.': ['setFrame', 'getFrame', 'x', 'y', 'width', 'height'],
        'time.': ['ticks_ms', 'ticks_diff', 'ticks_add', 'sleep_ms']
    };
    let lines;
    const providerCalls = [];
    const fake = {
        Uri: {
            file: fsPath => ({fsPath}),
            joinPath: (uri, ...parts) => ({fsPath: path.join(uri.fsPath, ...parts)})
        },
        Position: class Position {
            constructor(line, character) { this.line = line; this.character = character; }
        },
        workspace: {
            workspaceFolders: [{name: 'clean', uri: {fsPath: workspace}}],
            openTextDocument: async uri => {
                lines = fs.readFileSync(uri.fsPath, 'utf8').split('\n');
                return {uri};
            }
        },
        window: {showTextDocument: async () => {}},
        languages: {getDiagnostics: () => []},
        DiagnosticSeverity: {Error: 0},
        commands: {
            registerCommand: () => ({dispose() {}}),
            executeCommand: async (command, uri, position) => {
                assert.equal(uri.fsPath, path.join(workspace, 'examples', 'kepoco-intellisense-check.py'));
                providerCalls.push(command);
                const line = lines[position.line];
                switch (command) {
                    case 'vscode.executeCompletionItemProvider': {
                        const prefix = line.slice(0, position.character);
                        assert.ok(completions[prefix], `Unexpected completion prefix: ${prefix}`);
                        return {items: completions[prefix].map(label => ({label}))};
                    }
                    case 'vscode.executeHoverProvider':
                        return [{contents: [{value: line.includes('getPixel(')
                            ? 'getPixel does not return a value (None)'
                            : 'drawFilledRectangle — thumbyGraphics.py:108'}]}];
                    case 'vscode.executeSignatureHelpProvider':
                        return {signatures: [{label: 'drawFilledRectangle(x, y, width, height, colour)'}]};
                    case 'vscode.executeDefinitionProvider':
                        return [{uri: {fsPath: path.join(workspace, 'typings', 'thumbyGraphics', '__init__.pyi')}}];
                    default:
                        assert.fail(`Unexpected provider command: ${command}`);
                }
            }
        }
    };
    Module._load = function(request, parent, isMain) {
        if (request === 'vscode') return fake;
        return originalLoad.call(this, request, parent, isMain);
    };
    try {
        assert.equal(fs.existsSync(path.join(workspace, '.vscode')), false);
        delete require.cache[entry];
        const api = require(entry).activate({subscriptions: [], extensionPath: root});
        const result = await api.verifyIntelliSense({silent: true, maxAttempts: 1});
        const report = path.join(workspace, '.vscode', 'kepoco-intellisense-report.json');
        assert.ok(fs.existsSync(report), 'Verification must create its report directory');
        assert.equal(result.passed, true);
        assert.deepEqual(JSON.parse(fs.readFileSync(report, 'utf8')), result);
        assert.equal(result.completionChecks.length, 7);
        assert.equal(providerCalls.filter(c => c === 'vscode.executeCompletionItemProvider').length, 7);
        assert.equal(providerCalls.filter(c => c === 'vscode.executeHoverProvider').length, 2);
        assert.ok(providerCalls.includes('vscode.executeSignatureHelpProvider'));
        assert.ok(providerCalls.includes('vscode.executeDefinitionProvider'));
    } finally {
        Module._load = originalLoad;
        delete require.cache[entry];
        if (previousModule) require.cache[entry] = previousModule;
        fs.rmSync(workspace, {recursive: true, force: true});
    }
});

test('activation registers all five commands without changing a workspace', async () => {
    const entry = path.join(root, 'extension.js');
    assert.ok(fs.existsSync(entry), 'Extension command handlers are missing');
    const Module = require('node:module');
    const originalLoad = Module._load;
    const registered = new Map();
    const fake = {commands: {registerCommand: (name, handler) => {
        registered.set(name, handler);
        return {dispose() {}};
    }}};
    Module._load = function(request, parent, isMain) {
        if (request === 'vscode') return fake;
        return originalLoad.call(this, request, parent, isMain);
    };
    try {
        delete require.cache[entry];
        const extension = require(entry);
        const context = {subscriptions: [], extensionPath: root};
        const api = extension.activate(context);
        assert.equal(registered.size, 5);
        assert.equal(context.subscriptions.length, 5);
        assert.equal(typeof api.verifyIntelliSense, 'function');
        assert.equal(typeof api.setupProject, 'function');
    } finally {
        Module._load = originalLoad;
    }
});
