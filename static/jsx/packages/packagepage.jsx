var PackagePage = React.createClass(
	{
		getInitialState: function()
		{
			var packageReleasesResultState = new ResultState();
			packageReleasesResultState.changed.addListener(this.forceUpdate.bind(this, null));
			
			return {
				packageReleases: this.props.packageReleases || [],
				
				packageReleasesResultState: packageReleasesResultState
			};
		},
		
		render: function()
		{
			return (
				<div style={ { width: "50%", margin: "8px auto" } }>
					<div style={ { float: "right" } }>
						<Button marginLeft="8px" visible={ currentUser.canDeletePackage(this.props.package) } href={ this.props.package.getBasePath() + "/delete" } icon="delete" text="Delete" />
						<Button marginLeft="8px" visible={ currentUser.canEditPackage(this.props.package)   } href={ this.props.package.getBasePath() + "/edit"   } icon="pencil" text="Edit" />
					</div>
					<h2>{ this.props.package.displayName || <Placeholder text="None" /> }</h2>
					<hr />
					<ContentBox>
						<div>
							<PackageFieldsView item={ this.props.package } />
							<hr />
							<b>Code:</b>
							<DirectoryTreeFieldsView item={ this.props.package.codeDirectoryTree } />
							<hr />
							<b>Resources:</b>
							<DirectoryTreeFieldsView item={ this.props.package.resourcesDirectoryTree } />
						</div>
					</ContentBox>
					<div style={ { float: "right" } }>
						<ResultStatus resultState={ this.state.packageReleasesResultState } style={ { marginRight: "4px" } } />
						<Button marginLeft="8px" visible={ currentUser.canCreatePackageRelease(this.props.package) } icon="box" text="Create" onClick={ this.handleCreatePackageReleaseClick } />
					</div>
					<h2>Releases</h2>
					<hr />
					<PackageReleaseTable package={ this.props.package } items={ this.state.packageReleases } />
				</div>
			);
		},
		
		componentWillReceiveProps: function(nextProps)
		{
			if (this.props.packageReleases != nextProps.packageReleases)
			{
				this.setPackageReleases(nextProps.packageReleases);
			}
		},
		
		setPackageReleases: function(packageReleases)
		{
			this.setState({ packageReleases: packageReleases });
		},
		
		updatePackageReleases: function()
		{
			this.state.packageReleasesResultState.pending();
			
			Knotcake.Web.Get (
				this.props.package.getBasePath() + "/releases/all.json",
				{},
				function(response)
				{
					this.state.packageReleasesResultState.success();
					this.setPackageReleases(response.map(PackageRelease.create));
				}.bind(this),
				function(jqXHR, _, error)
				{
					this.state.packageReleasesResultState.failure(jqXHR.status + " " + error);
				}.bind(this)
			);
		},
		
		handleCreatePackageReleaseClick: function(event)
		{
			if (this.state.packageReleasesResultState.isPending()) { return; }
			
			this.state.packageReleasesResultState.pending();
			
			Knotcake.Web.Post(
				this.props.package.getBasePath() + "/releases/create",
				null,
				function(response)
				{
					if (response.success)
					{
						this.updatePackageReleases();
					}
					else
					{
						this.state.packageReleasesResultState.failure(response.message);
					}
				}.bind(this),
				function(jqXHR, _, error)
				{
					this.state.packageReleasesResultState.failure(jqXHR.status + " " + error);
				}.bind(this)
			);
		}
	}
);
