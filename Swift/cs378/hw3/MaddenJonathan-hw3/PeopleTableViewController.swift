//
//  PeopleTableViewController.swift
//  MaddenJonathan-hw3
//
//  Created by John Madden on 2/11/17.
//  Copyright © 2017 cs378. All rights reserved.
//

import UIKit
class PeopleTableViewController: UITableViewController {
    private var people = [Person]()
    
    // Intializes people list and sets Navigation title
    override func viewDidLoad() {
        super.viewDidLoad()
        self.title = "Person List"
        createDataModel()
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }

    // Set sections equal to one
    override func numberOfSections(in tableView: UITableView) -> Int {
        return 1
    }

    // Sets the number of rows in the table view to the number of people in the people list
    override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return people.count
    }

    // Adds details to the table view
    override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "cellid", for: indexPath)
        cell.textLabel?.text = "\(people[indexPath.row].firstName)"
        cell.detailTextLabel?.text = "\(people[indexPath.row].lastName)"
        return cell
    }
    
    // Add people to the people list
    func createDataModel() {
        people.append(Person(firstName:"Bob", lastName:"Carpenter", age:35, city:"Austin"))
        people.append(Person(firstName:"John", lastName:"Jones", age:8, city:"Boston"))
        people.append(Person(firstName:"Led", lastName:"Zeppelin", age:73, city:"Paris"))
        people.append(Person(firstName:"Sam", lastName:"Smith", age:34, city:"Sydney"))
        people.append(Person(firstName:"June", lastName:"Johnson", age:12, city:"Vienna"))
        people.append(Person(firstName:"Allison", lastName:"Atwater", age:21, city:"Venice"))
        people.append(Person(firstName:"Donald", lastName:"Trump", age:56, city:"Munich"))
        people.append(Person(firstName:"Hillary", lastName:"Clinton", age:69, city:"Brussels"))
        people.append(Person(firstName:"Barrack", lastName:"Obama", age:53, city:"Tokyo"))
        people.append(Person(firstName:"Teddy", lastName:"Roosevelt", age:70, city:"Shanghai"))
    }

    // Send information for the Person View Controller to print information correctly
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        let indexPath: Int = (self.tableView.indexPathForSelectedRow?.row)!
        let data = people[indexPath]
        if let destinationViewController = segue.destination as? PersonViewController {
            destinationViewController.person = data
        }
    }
}
