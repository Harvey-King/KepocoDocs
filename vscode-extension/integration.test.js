'use strict';
// Launched only by VS Code's extension test host, not on the device.
const vscode = require('vscode');
const fs = require('node:fs/promises');
const path = require('node:path');
const assert = require('node:assert/strict');

async function run() {
    const folder = vscode.workspace.workspaceFolders[0];
    const resultPath = path.join(folder.uri.fsPath, '.vscode', 'live-verification.json');
    await fs.mkdir(path.dirname(resultPath), {recursive: true});
    try {
        const extension = vscode.extensions.getExtension('kepoco-local.kepoco-devkit');
        assert.ok(extension, 'Development extension is not registered in VS Code');
        const api = await extension.activate();
        const result = await api.verifyIntelliSense({silent: true, maxAttempts: 45});
        await fs.writeFile(resultPath, JSON.stringify(result, null, 2), 'utf8');
        assert.ok(result.passed, 'One or more real IntelliSense providers failed; see live-verification.json');
        console.log('PASS: actual VS Code completion, hover, signature and definition providers.');
    } catch (error) {
        await fs.writeFile(resultPath, JSON.stringify({passed: false, error: String(error), stack: error.stack}, null, 2), 'utf8');
        throw error;
    }
}
module.exports = {run};
