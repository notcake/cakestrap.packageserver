var svnRepositoryTreeFields = [
	new Knotcake.OOP.Field()
		.setName("url")
		.setProperty("label", "SVN Repository URL:")
		.setProperty("placeholder", "svn://svn.metastruct.org/metastruct/")
		.setProperty("validator", NonNullableValidator("a URL", true)),
	new Knotcake.OOP.Field()
		.setName("revision")
		.setProperty("label", "Revision"),
	new Knotcake.OOP.Field()
		.setName("directory")
		.setProperty("label", "Directory")
		.setProperty("placeholder", "trunk")
];

var SvnRepositoryTreeFieldsView   = FieldsViewFactory(svnRepositoryTreeFields);
var SvnRepositoryTreeFieldsEditor = FieldsEditorFactory(svnRepositoryTreeFields);
