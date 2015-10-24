var PackagePage = React.createClass(
	{
		render: function()
		{
			return (
				<div style={ { width: "50%", margin: "8px auto" } }>
					<h2>{ this.props.package.displayName }</h2>
					<hr />
					<div style={ { overflow: "auto", width: "100%", margin: "8px auto", padding: "16px", backgroundColor: "beige" } }>
						<div>
							<h2>{ this.props.package.name }</h2>
							<hr />
							<TextFieldRow label="Name:"         text={ this.props.package.name        } />
							<TextFieldRow label="Display name:" text={ this.props.package.displayName } />
							<TextFieldRow label="Description:"  text={ this.props.package.description } />
							<hr />
							<TextFieldRow label="Git Repository URL:" text={ this.props.packageGitRepository && this.props.packageGitRepository.url       } />
							<TextFieldRow label="Branch:"             text={ this.props.packageGitRepository && this.props.packageGitRepository.branch    } />
							<TextFieldRow label="Revision:"           text={ this.props.packageGitRepository && this.props.packageGitRepository.revision  } />
							<TextFieldRow label="Directory:"          text={ this.props.packageGitRepository && this.props.packageGitRepository.directory } />
						</div>
					</div>
				</div>
			);
		}
	}
);
