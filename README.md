# Openhab Alfred Workflow
Workflow to control openhab from Alfred

![Openhab Workflow](./screenshot.png "Openhab Workflow")

## Download
[Openhab-1.0.0.alfredworkflow](https://raw.githubusercontent.com/digitalbirdo/alfred-openhab-workflow/master/Openhab-1.0.0.alfredworkflow)

## Changelog
### [not yet released](https://raw.githubusercontent.com/digitalbirdo/alfred-openhab-workflow/master)
* Autoload all available switch items when config is empty

### [1.0.0](https://raw.githubusercontent.com/digitalbirdo/alfred-openhab-workflow/master/Openhab-1.0.0.alfredworkflow)
* Initial Creation


## Configuration
The workflow initializes itself if no Workflow Environment Variables were set inside the workflow settings in Alfred before the first execution. (See [Using Variables in Workflows](https://www.alfredapp.com/help/workflows/advanced/variables/) for more details)

The following variables have to be set according to the Openhab installation:

* `OH_HOST` = IP Address of Openhab
* `OH_PORT` = Port on which Openhab is running
* `OH_USER` = User for Openhab (Empty if no Password)
* `OH_PASSWORD` = Password for Openhab (Empty if no Password)

Own Switches can also be added through the Alfred settings.
The `Name` of the variable in the Alfred settings will be the `Label` which is later shown in the alfred dialog and the `Value` has to match to an `itemname` which has to be present in your Openhab sitemap.

If no items are configured, the default sitemap will be scanned for all available switch items which are then added automatically.

## TODO's
* Load the Label of the items from the sitemap
* Support for other Items (e.g. Dimmer, ColorPicker, ...)

## Licencing & thanks

This workflow is released under the [MIT Licence](https://github.com/digitalbirdo/alfred-openhab-workflow/blob/master/LICENSE.md).

It uses the following libraries and resources:

* [Alfred-Workflow](https://github.com/deanishe/alfred-workflow) (MIT Licence) by deanishe for the workflow stuff.
* [Alfred Workflow Builder](https://gist.github.com/deanishe/b16f018119ef3fe951af) (MIT Licence) by deanishe. Build Alfred Workflows into .alfredworkflow (zip) files
* [Requests](https://github.com/kennethreitz/requests) (Apache License, Version 2.0) for the REST-API
* [Openhab REST-API Examples](https://github.com/openhab/openhab/wiki/Samples-REST) from Openhab Wiki
* The icon from [Openhab](https://github.com/openhab/openhab) (Eclipse Public License - v 1.0)