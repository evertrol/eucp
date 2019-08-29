import {
  JupyterFrontEnd, JupyterFrontEndPlugin
} from '@jupyterlab/application';

import {
	IMainMenu
} from '@jupyterlab/mainmenu';

import {
	Menu
} from '@phosphor/widgets';

function activate(app: JupyterFrontEnd, mainMenu: IMainMenu) {
    console.log('$> JupyterLab extension Supercell is activated!');

	let submenu = new Menu(app);
	submenu.title.label = "Supercell...";

	const commands = {
		'add': 'notebook:edit-supercell-add',
		'remove': 'notebook:edit-supercell-remove'
	};

	app.commands.addCommand(commands['add'], {
		label: 'Add Current Cell',
		execute: () => {
			console.log('$> Adding cell');
		}
	});

	app.commands.addCommand(commands['remove'], {
		label: 'Remove Current Cell',
		execute: () => {
			console.log('$> Removing cell');
		}
	});

	submenu.addItem({
        command: commands['add'],
        args: {},
    });

	submenu.addItem({
        command: commands['remove'],
        args: {},
    });

	const submenuGroup = [
        { type: 'submenu', submenu: submenu } as Menu.IItemOptions
    ];

	mainMenu.editMenu.addGroup(submenuGroup, 40);

	console.log('$> ', submenu, submenuGroup);
}

/**
 * Initialization data for the Supercell extension.
 */
const extension: JupyterFrontEndPlugin<void> = {
	id: 'Supercell',
	autoStart: true,
	requires: [IMainMenu],
	activate: activate
};

export default extension;
