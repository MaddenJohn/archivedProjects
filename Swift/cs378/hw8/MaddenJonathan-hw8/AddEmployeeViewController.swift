//
//  AddEmployeeViewController.swift
//  MaddenJonathan-hw8
//
//  Created by John Madden on 4/5/17.
//  Copyright © 2017 cs378. All rights reserved.
//

import UIKit

// Class for adding to the array
class AddEmployeeViewController: UIViewController {
    @IBOutlet weak var fName: UITextField!
    @IBOutlet weak var lName: UITextField!
    @IBOutlet weak var department: UITextField!
    @IBOutlet weak var jobTitle: UITextField!
    var alertController:UIAlertController? = nil

    override func viewDidLoad() {
        super.viewDidLoad()
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    @IBAction func buttonHandler(_ sender: Any) {
        // Get the data from the text fields
        let data1 = fName.text!
        let data2 = lName.text!
        let data3 = department.text!
        let data4 = jobTitle.text!
        
        // package the data into a dictionary
        let dataDict = ["data1":data1, "data2":data2, "data3":data3, "data4":data4];
        
        NotificationCenter.default.post(name: Notification.Name(rawValue: "event1Key"), object: nil, userInfo: dataDict)
        
        // Alert for when adding data
        self.alertController = UIAlertController(title: "Add Employee", message: "Employee has been added!!", preferredStyle: UIAlertControllerStyle.alert)
        
        let OKAction = UIAlertAction(title: "OK", style: UIAlertActionStyle.default) { (action:UIAlertAction) in
            print("Ok Button Pressed 1");
        }
        self.alertController!.addAction(OKAction)
        self.present(alertController!, animated: true, completion: nil)
    }
}
