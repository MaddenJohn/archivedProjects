//
//  ShowEmployeeTableViewController.swift
//  MaddenJonathan-hw8
//
//  Created by John Madden on 4/5/17.
//  Copyright © 2017 cs378. All rights reserved.
//

import UIKit

// Custom class for displaying the table view
class ShowEmployeeTableViewController: UITableViewController {
    var employees = [Employee]()

    override func viewDidLoad() {
        super.viewDidLoad()
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
    
    override func numberOfSections(in tableView: UITableView) -> Int {
        return 1
    }

    override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return employees.count
    }

    // Set appropriate protocals for custom cell
    override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "cellid", for: indexPath) as! ShowEmployeeTableViewCell
        cell.fName.text = employees[indexPath.row].firstName
        cell.lName.text = employees[indexPath.row].lastName
        cell.dept.text = employees[indexPath.row].department
        cell.title.text = employees[indexPath.row].jobTitle
        return cell
    }
}
