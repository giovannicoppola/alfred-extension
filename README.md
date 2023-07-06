WeWorkflow
================

An [Alfred](https://www.alfredapp.com/) workflow to quickly access and manage other workflows' info and folders. 
Derived from `alfred-extension`, an [Alfred2 extension](https://github.com/jmjeong/alfred-extension/tree/master/managealfredextension) created by 
Jaemok Jeong ([jmjeong](https://github.com/jmjeong)). 

Main changes: dropped `open in iTerm2`, `export`, and `disable` actions, added access to workflow info, folder, and cache, config, detection of hotkey conflicts. Workflows' info now stored in a `sqlite` database for faster access.

![](images/alfred-weworkflow.gif)

<a href="https://github.com/giovannicoppola/alfred-weworkflow/releases/latest/">
<img alt="Downloads"
src="https://img.shields.io/github/downloads/giovannicoppola/alfred-weworkflow/total?color=purple&label=Downloads"><br/>
</a>

<!-- MarkdownTOC autolink="true" bracket="round" depth="3" autoanchor="true" -->

- [Setting up](#setting-up)
- [Basic Usage](#usage)
- [Known Issues](#known-issues)
- [Acknowledgments](#acknowledgments)
- [Changelog](#changelog)
- [Feedback](#feedback)


<h1 id="setting-up">Setting up ⚙️</h1>

### Needed

- Alfred with Powerpack license
- Python3 (howto install [here](https://www.freecodecamp.org/news/python-version-on-mac-update/))

### Setup
  
1. Download the most recent release of `alfred-WeWorkflow` from [Github](https://github.com/giovannicoppola/alfred-weworkflow/releases/latest) and double-click to install
2. _Optional:_ Setup a hotkey to launch `alfred-WeWorkflow`
4. _Optional:_ Change the keyword to launch `alfred-WeWorkflow` (currently set to `ww`)


<h1 id="usage">Basic Usage 📖</h1>

`ww` or hotkey will launch `WeWorkflow`, type to search workflows (or use `advanced search` below. 

1. `return (⏎)` will open the workflow folder in Alfred's file browser
2. `shift-return (⇧⏎)` will show the Workflow's **config** screen in Alfred
3. `control-return (⌃⏎)` will show the Workflow's **info** in large font (including hotkey conflicts with active 🔴 and disabled 🟠 workflows)
4. `command-return (⌘⏎)` will open the Workflow's **folder** in Finder
5. `command-shift-return (⌘⇧⏎)` will open the Workflow's **folder** in Terminal
6. `option-return (⌥⏎)` will open the Workflow's **cache folder** (if existing) in Finder
7. `option-shift-return (⌥⇧⏎)` will open the Workflow's **cache folder** (if existing) in Terminal
8. `fn-return (fn⏎)` will **launch** the workflow with the first keyword
9. `control-option-shift-return (^⌥⇧⏎)` will open the Workflow's **data folder** (if existing) in Finder



## Advanced search 🔍
- enter `field:`, where `field` is any of the fields below. Example: `name:wework`
	- `name`
	- `author`
	- `keywords`
	- `hotkeys`
	- `disabled` (i.e. `disabled:true` and `disabled:false`)
	- `description`
	- `category`
	- `readme`




<h1 id="known-issues">Known issues ⚠️</h1>

- None for now, but let me know if you see anything!

<h1 id="acknowledgments">Acknowledgments 😀</h1>

- Jaemok Jeong ([jmjeong](https://github.com/jmjeong)) for developing [alfred extension](https://github.com/jmjeong/alfred-extension/tree/master/managealfredextension).
- The [Alfred forum](https://www.alfredforum.com) community.

<h1 id="changelog">Changelog 🧰</h1>

- 07-06-2023: version 1.3 (faster open config)
- 03-02-2023: version 1.2 (adding option to open the data folder)
- 12-04-2022: version 1.1 (Alfred 5)
- 04-17-2022: version 1.0

<h1 id="feedback">Feedback 🧐</h1>

Feedback welcome! If you notice a bug, or have ideas for new features, please feel free to get in touch either here, or on the [Alfred](https://www.alfredforum.com) forum. 