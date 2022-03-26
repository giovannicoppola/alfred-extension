## Manage Alfred Extension ([Download](https://raw.github.com/jmjeong/alfred-extension/master/managealfredextension/ManageAlfredExtension.alfredworkflow))

Browse and manage the installed extension

![Demo screenshot](https://raw.github.com/jmjeong/alfred-extension/master/managealfredextension/screenshot.png)

###  Usage

```
 alf                :: display the installed extensions
 alf <search>       :: search extension by title, author name, and keyword

 enter              :: Browse the installed folder in Alfred
 ctrl               :: Reveal the installed folder in Finder
 shift              :: Execute extension with the first keyword
 cmd                :: Open terminal in the installed folder
 shift              :: Export the extension for distribution 
                       (Default: ~/Downloads, you can customize it with export.json file)
 fn                 :: Enable or Disable an extension
```

### export.json 

The file format is as follows:

```json
{
    "workflow-export" :
	    {"directory" : "~/git/alfred-extension/managealfredextension",
		 "enable": true},
    "source-export":
		{"directory" : "~/git/alfred-extension/managealfredextension",
		 "enable": false}
}
```

*'workflow-export'* specifies the directory where <extension>.alfredworkflow is exported.
*'source-export'* specifies the directory where extension source is copied.  

If there is no '*export.json*' file or there is an error in '*export.json*' file, 
*~/Downloads* directory is used for workflow export.


### Version History

#### 2.12 - July 26, 2016

- Open iTerm2 with existing windows (Thanks nikitavoloboev)

#### 2.11 - May 22, 2016

- Update for Alfred 3
- Change default terminal app into iTerm 2

#### 2.10 - Apr 19, 2015

- escape path in 'open terminal' command 

#### 2.9 - July 17, 2014

- case insensitive search

#### 2.8 - July 16, 2014

- Handles the title and author having space properly

#### 2.7 - April 19, 2013

- UUID is now optional for alfred 2.0.3

#### 2.6 - April 11, 2013

- Handle subdirectory during export

#### 2.5 - April 8, 2013

- Display hotkey information 
  - Hotkey information is borrowed from (com.help.shawn.rice) by Shawn Rice

#### 2.4 - April 1, 2013

- Fix a bug about pathname with space

#### 2.3 - March 31, 2013

- Sort title by alphabetically

#### 2.2 - March 29, 2013

- Export feature : Default directory is ~/Downloads
- Toggle extensions with fn modifier
- Fix a bug in export function

#### 2.0 - March 29, 2013

- Export feature
- Open terminal 
- Support Alleyoop's auto update plugin
- Display 'disabled' extension

#### 1.x - March 28, 2013

- Initial version
