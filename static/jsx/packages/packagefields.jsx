var packageFields = [
	new Knotcake.OOP.Field()
		.setName("name")
		.setProperty("label", "Name")
		.setProperty("placeholder", "net.minecraft.server")
		.setProperty("validator",
			function(package, value, validationCallback)
			{
				if (value == "")
				{
					validationCallback(false, "You must provide a package name!");
					return;
				}
				
				Knotcake.Web.Get(
					"/packages/named.json",
					{ name: value },
					function(response)
					{
						if (response == null) { validationCallback(true); return; }
						if (response.id == package.id) { validationCallback(true); return; }
						
						validationCallback(false, "A package with this name already exists!");
					},
					function(jqXHR, _, error)
					{
						validationCallback(false, jqXHR.status + " " + error);
					}
				);
			}
		)
		.setProperty("onTextChanged",
			function(package, value)
			{
				if (package.displayName == package.name)
				{
					package.displayName = value;
					this.forceUpdate();
					this.validate("displayName", value);
				}
				
				package.name = value;
			}
		),
	new Knotcake.OOP.Field()
		.setName("displayName")
		.setProperty("label", "Display name")
		.setProperty("validator", NonNullableValidator("a display name", true)),
	new Knotcake.OOP.Field()
		.setName("description")
		.setProperty("label", "Description")
		.setProperty("multiline", true)
		.setProperty("validator", NonNullableValidator("a description", true))
];

var PackageFieldsView   = FieldsViewFactory(packageFields);
var PackageFieldsEditor = FieldsEditorFactory(packageFields);
