'use strict';

function settingsPlan(current = {}) {
    return {
        stubPath: './typings',
        extraPaths: [...new Set([...(current.extraPaths || []), './vendor/micropython'])],
        autoImportCompletions: true,
        typeCheckingMode: current.typeCheckingMode === 'strict' ? 'strict' : 'basic',
        diagnosticSeverityOverrides: {
            ...(current.diagnosticSeverityOverrides || {}),
            // Runtime modules live on the device, not in desktop Python.
            // Missing imports, undefined names and argument errors are NOT disabled.
            reportMissingModuleSource: 'none'
        }
    };
}

module.exports = {settingsPlan};
