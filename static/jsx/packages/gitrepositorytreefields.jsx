var gitRepositoryTreeFields = [
	new Knotcake.OOP.Field()
		.setName("url")
		.setProperty("label", "Git Repository URL:")
		.setProperty("placeholder", "https://github.com/notcake/glib.git")
		.setProperty("validator", NonNullableValidator("a URL", true)),
	new Knotcake.OOP.Field()
		.setName("branch")
		.setProperty("label", "Branch")
		.setProperty("placeholder", "master"),
	new Knotcake.OOP.Field()
		.setName("revision")
		.setProperty("label", "Revision"),
	new Knotcake.OOP.Field()
		.setName("directory")
		.setProperty("label", "Directory")
];

var GitRepositoryTreeFieldsView   = FieldsViewFactory(gitRepositoryTreeFields);
var GitRepositoryTreeFieldsEditor = FieldsEditorFactory(gitRepositoryTreeFields);
