var PackageReleasePage = React.createClass(
	{
		render: function()
		{
			return (
				<div style={ { width: "50%", margin: "8px auto" } }>
					<div style={ { float: "right" } }>
						<Button marginLeft="8px" href={ this.props.packageRelease.getBasePath() + "/download" } icon="basket_put" text="Download" />
						<Button marginLeft="8px" visible={ currentUser.canDeletePackageRelease(this.props.package, this.props.packageRelease) } href={ this.props.packageRelease.getBasePath() + "/delete?returnPage=packageRelease" } icon="delete" text="Delete" />
					</div>
					<h2>
						<a href={ this.props.package.getBasePath() }>
							{ this.props.package.displayName || <Placeholder text="None" /> }
						</a>
						{ " Version " }
						{ this.props.packageRelease.versionName || <Placeholder text="None" /> }
					</h2>
					<hr />
					<ContentBox>
						<div>
							<PackageReleaseFieldsView item={ this.props.packageRelease } />
							<hr />
							<b>Code:</b>
							<DirectoryTreeFieldsView item={ this.props.packageRelease.codeDirectoryTree } />
							<hr />
							<b>Resources:</b>
							<DirectoryTreeFieldsView item={ this.props.packageRelease.resourcesDirectoryTree } />
						</div>
					</ContentBox>
					<h2>Data</h2>
					<hr />
					<ContentBox>
						<HexView ref="hexView" />
					</ContentBox>
				</div>
			);
		},
		
		componentDidMount: function()
		{
			Knotcake.Web.GetBinary(
				this.props.packageRelease.getBasePath() + "/download",
				{},
				function(response)
				{
					var fileReader = new FileReader();
					fileReader.readAsArrayBuffer(response);
					fileReader.onload = function(event)
					{
						this.refs.hexView.setData(fileReader.result);
					}.bind(this);
				}.bind(this),
				function(jqXHR, _, error)
				{
					this.state.packageReleasesResultState.failure(jqXHR.status + " " + error);
				}.bind(this)
			);
		}
	}
);
