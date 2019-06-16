//
//  AddCandidateViewController.swift
//  MaddenJonathan-hw5
//
//  Created by John Madden on 2/22/17.
//  Copyright © 2017 cs378. All rights reserved.
//

import UIKit
import CoreData

class AddCandidateViewController: UIViewController {
    @IBOutlet weak var firstNameTextField: UITextField!
    @IBOutlet weak var lastNameTextField: UITextField!
    @IBOutlet weak var stateTextField: UITextField!
    @IBOutlet weak var segmentedControl: UISegmentedControl!
    @IBOutlet weak var labelText: UILabel!
    
    var people = [NSManagedObject]()
    var party:String!
    var partyIndex:Int!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        labelText.text = ""
        self.segmentedControl.selectedSegmentIndex = 0
        self.title = "Add Candidate"
        self.party = "Democrat"
        self.partyIndex = 0
    }
    
    // This function is taken from the class code for resolving
    // problems with the entity.
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        
        let appDelegate = UIApplication.shared.delegate as! AppDelegate
        let managedContext = appDelegate.persistentContainer.viewContext
        let fetchRequest = NSFetchRequest<NSFetchRequestResult>(entityName:"Person")
        var fetchedResults:[NSManagedObject]? = nil
        
        do {
            try fetchedResults = managedContext.fetch(fetchRequest) as? [NSManagedObject]
        } catch {
            // what to do if an error occurs?
            let nserror = error as NSError
            NSLog("Unresolved error \(nserror), \(nserror.userInfo)")
            abort()
        }
        
        if let results = fetchedResults {
            people = results
        } else {
            print("Could not fetch")
        }
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    // Handler for Segmented Control
    @IBAction func segmentHandler(_ sender: Any) {
        self.partyIndex = self.segmentedControl.selectedSegmentIndex
        self.setTwoOptions()
    }
    
    // Function to handle SegmentedControl
    func setTwoOptions() {
        switch self.segmentedControl.selectedSegmentIndex
        {
        case 0:
            self.party = "Democrat"
        case 1:
            self.party = "Republican"
        default:
            break
        }
    }
    
    // Handler for when the button is pressed. This calls the savePerson function 
    // if the input is valid to commit this person to core data.
    @IBAction func btnHandler(_ sender: Any) {
        
        if (firstNameTextField.text == "" || lastNameTextField.text == "" || stateTextField.text == ""){
            labelText.text = "You must enter a value for all fields."
        }
        else {
            labelText.text = "Candidate Saved!"
            savePerson(firstName:firstNameTextField.text!, lastName:lastNameTextField.text!, state:stateTextField.text!)
        }
    }
    
    // Saves this person created to the core data. Much of this
    // code has been replicated from the code given in class, such as
    // the error checking for checking the managedContext.
    func savePerson(firstName: String, lastName: String, state: String) {
        
        let appDelegate = UIApplication.shared.delegate as! AppDelegate
        let managedContext = appDelegate.persistentContainer.viewContext
        
        // Create the entity we want to save
        let entity =  NSEntityDescription.entity(forEntityName: "Person", in: managedContext)
        
        let person = NSManagedObject(entity: entity!, insertInto:managedContext)
        
        // Set the attribute values
        person.setValue(firstName, forKey: "firstName")
        person.setValue(lastName, forKey: "lastName")
        person.setValue(state, forKey: "state")
        person.setValue(party, forKey: "party")
        
        // Commit the changes.
        do {
            try managedContext.save()
        } catch {
            // what to do if an error occurs?
            let nserror = error as NSError
            NSLog("Unresolved error \(nserror), \(nserror.userInfo)")
            abort()
        }
        
        // Add the new entity to our array of managed objects
        people.append(person)
    }
}
