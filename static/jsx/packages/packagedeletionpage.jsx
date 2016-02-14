var PackageDeletionPage = React.createClass(
	{
		getInitialState: function()
		{
			var submissionResultState = new ResultState();
			submissionResultState.changed.addListener(this.forceUpdate.bind(this, null));
			
			return {
				submissionResultState: submissionResultState
			};
		},
		
		render: function()
		{
			return (
				<div style={ { width: "50%", margin: "8px auto" } }>
					<h2>{ "Delete Package" }</h2>
					<hr />
					{ "Are you sure you want to delete package " + this.props.package.name + "?" }
					<hr />
					<div style={ { textAlign: "right" } }>
						<ResultStatus resultState={ this.state.submissionResultState } style={ { marginRight: "4px" } } />
						<Button marginLeft="8px" text={ "Cancel" } onClick={ this.handleCancelClick } />
						<Button className="btn-danger" marginLeft="8px" icon={ "delete" } text={ "Delete" } onClick={ this.handleDeleteClick } />
					</div>
				</div>
			);
		},
		
		handleCancelClick: function(event)
		{
			window.location.href = this.props.package.getBasePath();
		},
		
		handleDeleteClick: function(event)
		{
			if (this.state.submissionResultState.isPending()) { return; }
			
			this.state.submissionResultState.pending();
			
			Knotcake.Web.Post(
				this.props.package.getBasePath() + "/delete",
				null,
				function(response)
				{
					if (response.success)
					{
						this.state.submissionResultState.success();
						window.location.href = "/packages/all";
					}
					else
					{
						this.state.submissionResultState.failure(response.message);
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
