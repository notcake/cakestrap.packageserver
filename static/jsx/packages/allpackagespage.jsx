var AllPackagesPage = React.createClass(
	{
		getInitialState: function()
		{
			return { viewMode: "grid" };
		},
		
		render: function()
		{
			var visiblePackageCount = 0;
			
			return (
				<div style={ { width: "50%", margin: "8px auto" } }>
					<div style={ { float: "right" } }>
						<Button visible={ currentUser.canCreatePackages() } href="/packages/create" icon="add" text="Add package" />
						<ButtonGroup style={ { marginLeft: "8px" } }>
							<Button icon="fa:th"   pressed={ this.state.viewMode == "grid" } onClick={ this.setViewMode.bind(this, "grid") } />
							<Button icon="fa:list" pressed={ this.state.viewMode == "list" } onClick={ this.setViewMode.bind(this, "list") } />
						</ButtonGroup>
					</div>
					<h2>Packages</h2>
					<hr />
					<GridListView viewMode={ this.state.viewMode } itemClass={ PackageGridListViewItem } items={ this.props.packages } />
				</div>
			);
		},
		
		setViewMode: function(viewMode)
		{
			if (this.state.viewMode == viewMode) { return; }
			
			this.setState({ viewMode: viewMode });
		}
	}
);
