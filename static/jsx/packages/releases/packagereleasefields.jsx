var packageReleaseFields = [
	new Knotcake.OOP.Field()
		.setName("versionTimestamp")
		.setProperty("label", "Created at:")
		.setProperty("formatter",
			function(packageRelease, timestamp)
			{
				return new Knotcake.DateTime(timestamp).toLongLocalString();
			}
		)
		.setProperty("noteFormatter",
			function(packageRelease, timestamp)
			{
				return new Knotcake.DateTime(timestamp).toRelativeTimeString();
			}
		),
	new Knotcake.OOP.Field()
		.setName("versionName")
		.setProperty("label", "Version")
		.setProperty("validator", NonNullableValidator("a version", true)),
];

var PackageReleaseFieldsView   = FieldsViewFactory(packageReleaseFields);
var PackageReleaseFieldsEditor = FieldsEditorFactory(packageReleaseFields);
