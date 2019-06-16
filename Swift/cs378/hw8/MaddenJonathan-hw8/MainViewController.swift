//
//  MainViewController.swift
//  MaddenJonathan-hw8
//
//  Created by John Madden on 4/5/17.
//  Copyright © 2017 cs378. All rights reserved.
//

import UIKit

// Main class for setting up Notifications and passing appropriate values
class MainViewController: UIViewController {
    var employees = [Employee]()
    override func viewDidLoad() {
        super.viewDidLoad()

        // Define an observer for the notification
        NotificationCenter.default.addObserver(self, selector: #selector(handler1(notification:)), name: NSNotification.Name(rawValue: "event1Key"), object: nil)
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
    
    deinit {
        // You need to remove the observer before this object goes away.
        // This removes all registered observers for this object.
        NotificationCenter.default.removeObserver(self)
    }
    
    // This handler definition has both the external and internal
    // argument name as 'notification'.
    func handler1(notification: Notification) {
        // extract the data that was sent in the notification
        let dataDict:Dictionary<String,String> = notification.userInfo as! Dictionary<String,String>
        
        let fName = dataDict["data1"]!
        let lName = dataDict["data2"]!
        let dep = dataDict["data3"]!
        let job = dataDict["data4"]!
        employees.append(Employee(firstName: fName, lastName: lName, department:dep, jobTitle:job))
    }

    // Set the protocal in the tableview controller with the array
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
        if let destinationViewController = segue.destination as? ShowEmployeeTableViewController {
            destinationViewController.employees = employees
        }
    }
}
