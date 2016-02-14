var PackageEditPage = React.createClass(
	{
		getInitialState: function()
		{
			var submissionResultState = new ResultState();
			submissionResultState.changed.addListener(this.forceUpdate.bind(this, null));
			
			var package = this.props.package || new Package();
			
			return {
				package:                package,
				codeDirectoryTree:      package.codeDirectoryTree      || new DirectoryTree(),
				resourcesDirectoryTree: package.resourcesDirectoryTree || new DirectoryTree(),
				
				submissionResultState: submissionResultState
			};
		},
		
		render: function()
		{
			var isCreation = this.state.package.id == null;
			var verb = isCreation ? "Create" : "Edit";
		
			return (
				<div style={ { width: "50%", margin: "8px auto" } }>
					<h2>{ verb + " Package" }</h2>
					<hr />
					<PackageFieldsEditor ref="package" item={ this.state.package } onEnter={ this.handlePackageFieldsEnter } />
					<hr />
					<b>Code:</b>
					<DirectoryTreeFieldsEditor ref="codeDirectoryTree"      item={ this.state.codeDirectoryTree      } onEnter={ this.handleCodeDirectoryTreeFieldsEnter      } />
					<hr />
					<b>Resources:</b>
					<DirectoryTreeFieldsEditor ref="resourcesDirectoryTree" item={ this.state.resourcesDirectoryTree } onEnter={ this.handleResourcesDirectoryTreeFieldsEnter }/>
					<hr />
					<div style={ { textAlign: "right" } }>
						<ResultStatus resultState={ this.state.submissionResultState } style={ { marginRight: "4px" } } />
						<Button marginLeft="8px" text={ "Cancel" } onClick={ this.handleCancelClick } />
						<Button className="btn-primary" marginLeft="8px" icon={ isCreation ? "add" : "disk" } text={ isCreation ? "Create" : "Save" } onClick={ this.handleSubmitClick } />
					</div>
				</div>
			);
		},
		
		handlePackageFieldsEnter:                function(event) { this.refs.codeDirectoryTree.select();      },
		handleCodeDirectoryTreeFieldsEnter:      function(event) { this.refs.resourcesDirectoryTree.select(); },
		handleResourcesDirectoryTreeFieldsEnter: function(event) { this.handleSubmitClick();                  },
		
		handleCancelClick: function(event)
		{
			var isCreation = this.state.package.id == null;
			
			if (isCreation)
			{
				window.location.href = "/packages/all";
			}
			else
			{
				window.location.href = this.state.package.getBasePath();
			}
		},
		
		handleSubmitClick: function(event)
		{
			if (this.state.submissionResultState.isPending()) { return; }
			
			var isCreation = this.state.package.id == null;
			
			this.refs.package.validate();
			this.refs.codeDirectoryTree.validate();
			this.refs.resourcesDirectoryTree.validate();
			
			this.state.submissionResultState.pending();
			
			Knotcake.Web.Post(
				isCreation ? "/packages/create" : (this.state.package.getBasePath() + "/edit"),
				{
					package:                this.state.package,
					codeDirectoryTree:      this.state.codeDirectoryTree,
					resourcesDirectoryTree: this.state.resourcesDirectoryTree
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
						this.refs.codeDirectoryTree.select(response.field);
						this.refs.resourcesDirectoryTree.select(response.field);
					}
				}.bind(this),
				function(jqXHR, _, error)
				{
					this.state.submissionResultState.failure(jqXHR.status + " " + error);
				}.bind(this)
			);
		}
	}
);
