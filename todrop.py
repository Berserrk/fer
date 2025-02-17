{
  "editor.fontFamily": "JetBrains Mono",
  "editor.fontSize": 14,
  "editor.fontLigatures": true,
  "notebook.output.fontFamily": "JetBrains Mono",
  "notebook.output.fontSize": 14,
  "editor.formatOnSave": true,
  "editor.suggest.insertMode": "replace",
  "terminal.integrated.fontFamily": "JetBrains Mono",
  "editor.linkedEditing": true,
  "javascript.updateImportsOnFileMove.enabled": "always",
  "window.zoomLevel": -1.623400328908832,
  "terminal.integrated.gpuAcceleration": "off",
  "window.commandCenter": false,
  "launch": {},
  "[json]": {},
  "editor.minimap.enabled": false,
  "workbench.iconTheme": "material-icon-theme",
  "update.showReleaseNotes": false,
  "zenMode.hideLineNumbers": false,
  "editor.lineNumbers": "relative",
  "vim.leader": "<Space>",
  "vim.hlsearch": true,
  "vim.normalModeKeyBindingsNonRecursive": [
    // NAVIGATION
    // switch b/w buffers
    {
      "before": [
        "<S-h>"
      ],
      "commands": [
        ":bprevious"
      ]
    },
    {
      "before": [
        "<S-l>"
      ],
      "commands": [
        ":bnext"
      ]
    },
    // splits
    {
      "before": [
        "leader",
        "v"
      ],
      "commands": [
        ":vsplit"
      ]
    },
    {
      "before": [
        "leader",
        "s"
      ],
      "commands": [
        ":split"
      ]
    },
    // panes
    {
      "before": [
        "leader",
        "h"
      ],
      "commands": [
        "workbench.action.focusLeftGroup"
      ]
    },
    {
      "before": [
        "leader",
        "j"
      ],
      "commands": [
        "workbench.action.focusBelowGroup"
      ]
    },
    {
      "before": [
        "leader",
        "k"
      ],
      "commands": [
        "workbench.action.focusAboveGroup"
      ]
    },
    {
      "before": [
        "leader",
        "l"
      ],
      "commands": [
        "workbench.action.focusRightGroup"
      ]
    },
    // NICE TO HAVE
    {
      "before": [
        "leader",
        "w"
      ],
      "commands": [
        ":w!"
      ]
    },
    {
      "before": [
        "leader",
        "q"
      ],
      "commands": [
        ":q!"
      ]
    },
    {
      "before": [
        "leader",
        "x"
      ],
      "commands": [
        ":x!"
      ]
    },
    {
      "before": [
        "[",
        "d"
      ],
      "commands": [
        "editor.action.marker.prev"
      ]
    },
    {
      "before": [
        "]",
        "d"
      ],
      "commands": [
        "editor.action.marker.next"
      ]
    },
    {
      "before": [
        "<leader>",
        "c",
        "a"
      ],
      "commands": [
        "editor.action.quickFix"
      ]
    },
    {
      "before": [
        "leader",
        "f"
      ],
      "commands": [
        "workbench.action.quickOpen"
      ]
    },
    {
      "before": [
        "leader",
        "p"
      ],
      "commands": [
        "editor.action.formatDocument"
      ]
    },
    {
      "before": [
        "g",
        "h"
      ],
      "commands": [
        "editor.action.showDefinitionPreviewHover"
      ]
    }
  ],
  "vim.visualModeKeyBindings": [
    // Stay in visual mode while indenting
    {
      "before": [
        "<"
      ],
      "commands": [
        "editor.action.outdentLines"
      ]
    },
    {
      "before": [
        ">"
      ],
      "commands": [
        "editor.action.indentLines"
      ]
    },
    // Move selected lines while staying in visual mode
    {
      "before": [
        "J"
      ],
      "commands": [
        "editor.action.moveLinesDownAction"
      ]
    },
    {
      "before": [
        "K"
      ],
      "commands": [
        "editor.action.moveLinesUpAction"
      ]
    },
    // toggle comment selection
    {
      "before": [
        "leader",
        "c"
      ],
      "commands": [
        "editor.action.commentLine"
      ]
    }
  ],
  "[typescriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "go.toolsManagement.autoUpdate": true,
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[jsonc]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "editor.cursorWidth": 4,
  "workbench.settings.applyToAllProfiles": [
    "workbench.colorCustomizations"
  ],
  "workbench.colorCustomizations": {
    "editorCursor.foreground": "#524e4c",
    "terminal.background": "#00000000"
  },
  "workbench.colorTheme": "Solarized Autumn",
  "terminal.integrated.defaultProfile.windows": "",
  "apc.header": {
    "height": 36
  },
  "apc.listRow": {
    "height": 24
  },
  "apc.styleSheet": { "stylesheet": Unknown word.
    ".title-label > h2": "display": "none",
    ".editor-actions": "display": "none",
    ".pane-body": "padding": "0 8px",
    ".pane-header": "padding": "0 8px",
  },
  "apc.electron": {
    "opacity": 0.45,
    "transparent": true,
    "backgroundColor": "#00000000",
    "vibrancy": "ultra-dark"
  }
}
