
describe('My first cypress test', () => {
	beforeEach(() => {
		// Cypress starts out with a blank slate for each test
		// so we must tell it to visit our website with the `cy.visit()` command.
		// Since we want to visit the same URL at the start of all our tests,
		// we include it in our beforeEach function so that it runs before each test
		cy.visit('127.0.0.1:8000')
		cy.get('input[name=email_id]').type("Dev@root.com",{force:true})
	
		// {enter} causes the form to submit
		cy.get('input[name=password]').type(`{hintuteslaClock`,{force:true})
		cy.get("#submit").click()
		// we should be redirected to /dashboard
		cy.url().should('include', '/home')

	})
	it('Checks the drag and drop features', function () {
		cy.visit('127.0.0.1:8000/Admin/table/5')
		cy.get("#clear_all_unlocked").click()

		cy.get('[subject_event_id=18]').then(el => {
			const draggable = el[0]  // Pick up this
			cy.get('#75_1').then(el => {
			  const droppable = el[0]  // Drop over this
		  
			  const coords = droppable.getBoundingClientRect()
			  draggable.dispatchEvent(new MouseEvent('mousemove'));
			  draggable.dispatchEvent(new MouseEvent('mousedown'));
			  draggable.dispatchEvent(new MouseEvent('mousemove', {clientX: 10, clientY: 0}));
			  draggable.dispatchEvent(new MouseEvent('mousemove', {clientX: coords.x+10, clientY: coords.y+10}));
			  draggable.dispatchEvent(new MouseEvent('mouseup'));
		  
			})
		  
		  })


		// cy.contains('Create', { timeout: 15000 })
		// let drop = cy.get("[timing_id=75]").children().eq(1)
		// drop.should('exist');
		// console.log(document.getElementById("clear_all_unlocked"))
		// cy.get("[subject_event_id=18]")
		// 	.should('exist')
		// 	.dragTo("#75_1")
		// cy.get("[subject_event_id=18]").trigger('drop',{force:true})
	})

})