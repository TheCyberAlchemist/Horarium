

describe('My first cypress test', () => {
	beforeEach(() => {
		// Cypress starts out with a blank slate for each test
		// so we must tell it to visit our website with the `cy.visit()` command.
		// Since we want to visit the same URL at the start of all our tests,
		// we include it in our beforeEach function so that it runs before each test
		cy.visit('127.0.0.1:8000')

	})
	it('logs in the page', function () {
		cy.get('input[name=email_id]').type("Dev@root.com",{force:true})
	
		// {enter} causes the form to submit
		cy.get('input[name=password]').type(`{hintuteslaClock`,{force:true})
		cy.get("#submit").click()
		// we should be redirected to /dashboard
		cy.url().should('include', '/home')

	})
	it('Checks the drag and drop features', function () {
		cy.visit('127.0.0.1:8000/Admin/table/5')
		
	})

})