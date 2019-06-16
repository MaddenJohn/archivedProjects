//
//  ContactTableViewController.swift
//  MaddenJonathan-hw4
//
//  Created by John Madden on 2/18/17.
//  Copyright © 2017 cs378. All rights reserved.
//

import UIKit

class ContactTableViewController: UITableViewController {
    private var people = [Person]()
    override func viewDidLoad() {
        super.viewDidLoad()
        self.title = "People List"
        createDataModel()
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
    
    // Add people to the people list
    func createDataModel() {
        people.append(Person(firstName:"Joe", lastName:"Johson", age:35, street:"1 Main Street", city:"Austin", state:"TX", zip:78128))
        people.append(Person(firstName:"Sam", lastName:"Smith", age:27, street:"2 Main Street", city:"Austin", state:"TX", zip:78228))
        people.append(Person(firstName:"Sue", lastName:"Jefferson", age:52, street:"3 Main Street", city:"Austin", state:"TX", zip:78328))
        people.append(Person(firstName:"Zoey", lastName:"Zimmerman", age:17, street:"4 Main Street", city:"Austin", state:"TX", zip:78428))
        people.append(Person(firstName:"Alan", lastName:"Albright", age:83, street:"5 Main Street", city:"Austin", state:"TX", zip:78528))
        people.append(Person(firstName:"Chris", lastName:"Chambers", age:33, street:"6 Main Street", city:"Austin", state:"TX", zip:78628))
        people.append(Person(firstName:"Danny", lastName:"Donaldson", age:6, street:"7 Main Street", city:"Austin", state:"TX", zip:78728))
        people.append(Person(firstName:"Eli", lastName:"Edgerton", age:10, street:"8 Main Street", city:"Austin", state:"TX", zip:78828))
        people.append(Person(firstName:"Frank", lastName:"Farmer", age:100, street:"9 Main Street", city:"Austin", state:"TX", zip:78928))
    }

    override func numberOfSections(in tableView: UITableView) -> Int {
        return 1
    }

    // Set the number two twice the people count, because there are two cells to be populated
    override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return people.count * 2
    }
    
    // This fuction will either set the appropriate variables for a NameTableViewCell or
    // set the variables for the AddressTableView cell, based on the indexPath.row
    override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let index = indexPath.row
        let personIndex = indexPath.row / 2
        
        if (index % 2 == 0){
            tableView.rowHeight = 50
            let cell = tableView.dequeueReusableCell(withIdentifier: "cellid", for: indexPath) as! NameTableViewCell
            cell.firstNameLabel?.text = people[personIndex].firstName
            cell.lastNameLabel?.text = people[personIndex].lastName
            cell.age = people[personIndex].age
            cell.viewControllerPoiner = self
            return cell
        }
        else {
            tableView.rowHeight = 55
            let cell = tableView.dequeueReusableCell(withIdentifier: "cellid2", for: indexPath) as! AddressTableViewCell
            cell.streetLabel?.text = people[personIndex].street
            cell.cityLabel?.text = people[personIndex].city
            cell.stateLabel?.text = people[personIndex].state
            cell.zipLabel?.text = "\(people[personIndex].zip)"
            return cell
        }
    }
}
