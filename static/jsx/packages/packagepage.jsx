var PackagePage = React.createClass(
	{
		render: function()
		{
			return (
				<div style={ { width: "50%", margin: "8px auto" } }>
					<div style={ { float: "right" } }>
						<Button visible={ currentUser.canEditPackage(this.props.package) } href={ "/packages/" + this.props.package.id + "/edit" } icon="pencil" text="Edit" />
					</div>
					<h2>{ this.props.package.displayName }</h2>
					<div style={ { clear: "both" } } />
					<hr />
					<div style={ { overflow: "auto", width: "100%", margin: "8px auto", padding: "16px", backgroundColor: "beige" } }>
						<div>
							<h2>{ this.props.package.name }</h2>
							<hr />
							<PackageFieldsView item={ this.props.package } />
							<hr />
							<PackageGitRepositoryFieldsView item={ this.props.packageGitRepository } />
						</div>
					</div>
				</div>
			);
		}
	}
);
