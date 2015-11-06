var PackageCreationPage = React.createClass(
	{
		getInitialState: function()
		{
			var submissionResultState = new ResultState();
			submissionResultState.changed.addListener(this.forceUpdate.bind(this, null));
			
			return {
				package: new Package(),
				packageGitRepository: new PackageGitRepository(),
				
				submissionResultState: submissionResultState
			};
		},
		
		render: function()
		{
			return (
				<div style={ { width: "50%", margin: "8px auto" } }>
					<h2>Create Package</h2>
					<hr />
					<PackageFieldsEditor ref="package" item={ this.state.package } onEnter={ this.handlePackageFieldsEnter } />
					<hr />
					<PackageGitRepositoryFieldsEditor ref="packageGitRepository" item={ this.state.packageGitRepository } onEnter={ this.handlePackageGitRepositoryFieldsEnter } />
					<hr />
					<div style={ { textAlign: "right" } }>
						<ResultStatus resultState={ this.state.submissionResultState } style={ { marginRight: "4px" } } />
						<Button icon="add" text="Create Package" onClick={ this.handleCreateClick } />
					</div>
				</div>
			);
		},
		
		handlePackageFieldsEnter:              function(event) { this.refs.packageGitRepository.select(); },
		handlePackageGitRepositoryFieldsEnter: function(event) { this.handleCreateClick();                },
		
		handleCreateClick: function(event)
		{
			if (this.state.submissionResultState.isPending()) { return; }
			
			this.refs.package.validate();
			this.refs.packageGitRepository.validate();
			
			this.state.submissionResultState.pending();
			
			$.post(
				"/packages/create",
				{
					name:             this.state.package.name,
					displayName:      this.state.package.displayName,
					description:      this.state.package.description,
					
					gitRepositoryUrl: this.state.packageGitRepository.url,
					gitBranch:        this.state.packageGitRepository.branch,
					gitRevision:      this.state.packageGitRepository.revision,
					gitDirectory:     this.state.packageGitRepository.directory
				},
				function(response)
				{
					if (response.success)
					{
						this.state.submissionResultState.success();
						window.location.href = "/packages/" + response.id.toString();
					}
					else
					{
						this.state.submissionResultState.failure(response.message);
						this.refs.package.select(response.field);
						this.refs.packageGitRepository.select(response.field);
					}
				}.bind(this)
			).fail(
				function(jqXHR, _, error)
				{
					this.state.submissionResultState.failure(jqXHR.status + " " + error);
				}.bind(this)
			);
		}
	}
);
