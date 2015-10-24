var PackageCreationPage = React.createClass(
	{
		getInitialState: function()
		{
			var nameValidator = new ValidationController();
			nameValidator.setValidator(
				function(value, validationCallback)
				{
					if (value == "")
					{
						validationCallback(false, "You must provide a package name!");
						return;
					}
					
					$.get(
						"/packages/named.json",
						{ name: value },
						function(response)
						{
							this.setState({ validatedName: name });
							
							validationCallback(response == null, response != null && "A package with this name already exists!");
						}.bind(this)
					).fail(
						function(jqXHR, _, error)
						{
							validationCallback(false, jqXHR.status + " " + error);
						}
					);
				}.bind(this)
			);
			
			var submissionResultState = new ResultState();
			submissionResultState.changed.addListener(this.forceUpdate.bind(this, null));
			
			return {
				name: "",
				displayName: "",
				description: "",
				
				gitRepositoryUrl: "",
				gitBranch: "",
				gitRevision: "",
				gitDirectory: "",
				
				nameValidator: nameValidator,
				
				submissionResultState: submissionResultState
			};
		},
		
		render: function()
		{
			return (
				<div style={ { width: "50%", margin: "8px auto" } }>
					<h2>Create Package</h2>
					<hr />
					<div>
						<TextEntryFormRow ref="name"        validationController={ this.state.nameValidator } label="Name:"         text={ this.state.name        } placeholder="net.minecraft.server"                                                            onTextChanged={ this.setName                               } onEnter={ this.handleNameEnter        } />
						<TextEntryFormRow ref="displayName"                                                   label="Display Name:" text={ this.state.displayName }                                    validator={ NonNullableValidator("a display name", true) } onTextChanged={ this.setProperty.bind(this, "displayName") } onEnter={ this.handleDisplayNameEnter } />
						<TextEntryFormRow ref="description"                                                   label="Description:"  text={ this.state.description }                                    validator={ NonNullableValidator("a description",  true) } onTextChanged={ this.setProperty.bind(this, "description") } multiline={ true } />
					</div>
					<hr />
					<div>
						<TextEntryFormRow ref="gitRepositoryUrl" label="Git Repository URL:" text={ this.state.gitRepositoryUrl } placeholder="https://github.com/notcake/glib.git" onTextChanged={ this.setProperty.bind(this, "gitRepositoryUrl") } onEnter={ this.handleGitRepositoryUrlEnter } />
						<TextEntryFormRow ref="gitBranch"        label="Branch:"             text={ this.state.gitBranch        } placeholder="master"                              onTextChanged={ this.setProperty.bind(this, "gitBranch")        } onEnter={ this.handleGitBranchEnter        } />
						<TextEntryFormRow ref="gitRevision"      label="Revision:"           text={ this.state.gitRevision      }                                                   onTextChanged={ this.setProperty.bind(this, "gitRevision")      } onEnter={ this.handleGitRevisionEnter      } />
						<TextEntryFormRow ref="gitDirectory"     label="Directory:"          text={ this.state.gitDirectory     }                                                   onTextChanged={ this.setProperty.bind(this, "gitDirectory")     } onEnter={ this.handleGitDirectoryEnter     } />
					</div>
					<hr />
					<div style={ { textAlign: "right" } }>
						<ResultStatus resultState={ this.state.submissionResultState } style={ { marginRight: "4px" } } />
						<Button icon="add" text="Create Package" onClick={ this.handleCreateClick } />
					</div>
				</div>
			);
		},
		
		setName: function(name)
		{
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
		
		handleNameEnter:             function(event) { this.refs.displayName.select();      },
		handleDisplayNameEnter:      function(event) { this.refs.description.select();      },
		handleDescriptionEnter:      function(event) { this.refs.gitRepositoryUrl.select(); },
		handleGitRepositoryUrlEnter: function(event) { this.refs.gitBranch.select();        },
		handleGitBranchEnter:        function(event) { this.refs.gitRevision.select();      },
		handleGitRevisionEnter:      function(event) { this.refs.gitDirectory.select();     },
		handleGitDirectoryEnter:     function(event) { this.handleCreateClick();            },
		
		handleCreateClick: function(event)
		{
			if (this.state.submissionResultState.isPending()) { return; }
			
			this.refs.name.validate();
			this.refs.displayName.validate();
			this.refs.description.validate();
			
			this.refs.gitRepositoryUrl.validate();
			this.refs.gitBranch.validate();
			this.refs.gitRevision.validate();
			this.refs.gitDirectory.validate();
			
			this.state.submissionResultState.pending();
			
			$.post(
				"/packages/create",
				{
					name:             this.state.name,
					displayName:      this.state.displayName,
					description:      this.state.description,
					
					gitRepositoryUrl: this.state.gitRepositoryUrl,
					gitBranch:        this.state.gitBranch,
					gitRevision:      this.state.gitRevision,
					gitDirectory:     this.state.gitDirectory
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
						this.refs[response.field].select();
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
