var PackageCreationPage = React.createClass(
	{
		getInitialState: function()
		{
			return {
				name: "",
				displayName: "",
				description: "",
				
				gitRepositoryUrl: "",
				gitBranch: "",
				gitRevision: "",
				gitDirectory: "",
				
				validatedName: "",
				nameValid: null,
				validatingName: false
			};
		},
		
		render: function()
		{
			return (
				<div style={ { width: "50%", margin: "8px auto" } }>
					<h2>Create Package</h2>
					<hr />
					<div>
						<div className="form-group" style={ { marginBottom: "8px", whiteSpace: "nowrap" } }>
							<FieldLabel text="Name:" style={ { color: "brown" } } />
							<div className={ this.state.nameValid == false ? "col-md-9 has-error" : this.state.nameValid == true ? "col-md-9 has-success" : "col-md-9 " } >
								<TextEntry ref="name" style={ { width: "100%" } } placeholder="net.minecraft.server" text={ this.state.name } onTextChanged={ this.setName } onEnter={ this.handleNameEnter } />
							</div>
							<div style={ { display: "inline-block" } }></div>
							<div className={ this.state.nameValid ? "has-success" : "has-error" } style={ { display: "inline-block", padding: "4px 8px" } }>
								<Icon icon="spinner" visible={ this.state.validatingName } />
								<Icon icon={ this.state.nameValid ? "tick" : "cross" } visible={ !this.state.validatingName && this.state.nameValid != null } />
								<span className="control-label" style={ { verticalAlign: "middle", marginLeft: "4px" } }>
									{ this.state.nameValid != false ? "" : this.state.name == "" ? "You must provide a package name!" : "This package already exists!" }
								</span>
							</div>
							<div style={ { clear: "both" } } />
						</div>
						<div className="form-group" style={ { marginBottom: "8px" } }>
							<FieldLabel text="Display Name:" />
							<div className="col-md-9">
								<TextEntry ref="displayName" style={ { width: "100%" } } text={ this.state.displayName } onTextChanged={ this.setProperty.bind(this, "displayName") } onEnter={ this.handleDisplayNameEnter } />
							</div>
							<div style={ { clear: "both" } } />
						</div>
						<div className="form-group" style={ { marginBottom: "8px" } }>
							<FieldLabel text="Description:" />
							<div className="col-md-9">
								<TextEntry ref="description" style={ { width: "100%" } } onTextChanged={ this.setProperty.bind(this, "description") } multiline={ true } />
							</div>
							<div style={ { clear: "both" } } />
						</div>
					</div>
					<hr />
					<div>
						<div className="form-group" style={ { marginBottom: "8px" } }>
							<FieldLabel text="Git Repository URL:" />
							<div className="col-md-9">
								<TextEntry ref="gitRepositoryUrl" style={ { width: "100%" } } placeholder="https://github.com/notcake/glib.git" onTextChanged={ this.setProperty.bind(this, "gitRepositoryUrl") } onEnter={ this.handleGitRepositoryUrlEnter } />
							</div>
							<div style={ { clear: "both" } } />
						</div>
						<div className="form-group" style={ { marginBottom: "8px" } }>
							<FieldLabel text="Branch:" />
							<div className="col-md-9">
								<TextEntry ref="gitBranch" style={ { width: "100%" } } placeholder="master" onTextChanged={ this.setProperty.bind(this, "gitBranch") } onEnter={ this.handleGitBranchEnter } />
							</div>
							<div style={ { clear: "both" } } />
						</div>
						<div className="form-group" style={ { marginBottom: "8px" } }>
							<FieldLabel text="Revision:" />
							<div className="col-md-9">
								<TextEntry ref="gitRevision" style={ { width: "100%" } } onTextChanged={ this.setProperty.bind(this, "gitRevision") } onEnter={ this.handleGitRevisionEnter } />
							</div>
							<div style={ { clear: "both" } } />
						</div>
						<div className="form-group" style={ { marginBottom: "8px" } }>
							<FieldLabel text="Directory:" />
							<div className="col-md-9">
								<TextEntry ref="gitDirectory" style={ { width: "100%" } } onTextChanged={ this.setProperty.bind(this, "gitDirectory") } onEnter={ this.handleGitDirectoryEnter } />
							</div>
							<div style={ { clear: "both" } } />
						</div>
					</div>
					<hr />
					<div style={ { textAlign: "right" } }>
						<Button icon="/static/images/silkicons/add.png" text="Create Package" onClick={ this.handleCreateClick } />
					</div>
				</div>
			);
		},
		
		setName: function(name)
		{
			if (this.state.name == this.state.validatedName)
			{
				this.dispatchNameValidation();
			}
			
			if (this.state.displayName == this.state.name)
			{
				this.setProperty("displayName", name);
			}
			
			this.setProperty("name", name);
		},
		
		setProperty: function(propertyName, propertyValue)
		{
			this.setState({ [propertyName]: propertyValue });
		},
		
		handleNameEnter: function(event)
		{
			if (this.state.validatingName == false &&
			    this.state.nameValid == null)
			{
				this.dispatchNameValidation();
			}
			
			this.refs.displayName.select();
		},
		
		handleDisplayNameEnter:      function(event) { this.refs.description.select();      },
		handleDescriptionEnter:      function(event) { this.refs.gitRepositoryUrl.select(); },
		handleGitRepositoryUrlEnter: function(event) { this.refs.gitBranch.select();        },
		handleGitBranchEnter:        function(event) { this.refs.gitRevision.select();      },
		handleGitRevisionEnter:      function(event) { this.refs.gitDirectory.select();     },
		handleGitDirectoryEnter:     function(event) { this.handleCreateClick();            },
		
		handleCreateClick: function(event)
		{
		},
		
		dispatchNameValidation: function()
		{
			this.setState({ validatingName: true })
			
			setTimeout(
				function()
				{
					var name = this.state.name;
					$.get(
						"/packages/named.json",
						{ name: name },
						function(response)
						{
							this.state.validatedName = name;
							
							if (this.state.name != this.state.validatedName)
							{
								this.dispatchNameValidation();
							}
							else
							{
								this.setState({ nameValid: response == null && name != "" });
								this.setState({ validatingName: false })
							}
						}.bind(this)
					);
				}.bind(this),
				200
			);
		}
	}
);
