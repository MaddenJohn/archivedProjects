//
//  PersonViewController.swift
//  MaddenJonathan-hw3
//
//  Created by John Madden on 2/11/17.
//  Copyright © 2017 cs378. All rights reserved.
//

import UIKit

class PersonViewController: UIViewController {
    // person holds the data to be printed in the Person View Controller
    var person:Person?
    // Each of these UILabels link to data held by person
    @IBOutlet weak var firstNameLabel: UILabel!
    @IBOutlet weak var ageLabel: UILabel!
    @IBOutlet weak var cityLabel: UILabel!
    @IBOutlet weak var lastNameLabel: UILabel!
    
    // Sets the Navigation title and each of the four labels to information in person
    override func viewDidLoad() {
        super.viewDidLoad()
        self.title = "Person"
        firstNameLabel.text = person?.firstName
        lastNameLabel.text = person?.lastName
        ageLabel.text = "\(person!.age)"
        cityLabel.text = person?.city
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
}
