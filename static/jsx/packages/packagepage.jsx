var PackagePage = React.createClass(
	{
		render: function()
		{
			return (
				<div style={ { width: "50%", margin: "8px auto" } }>
					<div style={ { float: "right" } }>
						<Button marginLeft="8px" visible={ currentUser.canDeletePackage(this.props.package) } href={ "/packages/" + this.props.package.id + "/delete" } icon="delete" text="Delete" />
						<Button marginLeft="8px" visible={ currentUser.canEditPackage(this.props.package)   } href={ "/packages/" + this.props.package.id + "/edit"   } icon="pencil" text="Edit" />
					</div>
					<h2>
						{
							this.props.package.displayName ?
								this.props.package.displayName :
								<span style={ { color: "gray", fontStyle: "italic" } }>{ "None" }</span>
						}
					</h2>
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
