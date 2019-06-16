//
//  CandidateDetailViewController.swift
//  MaddenJonathan-hw5
//
//  Created by John Madden on 2/23/17.
//  Copyright © 2017 cs378. All rights reserved.
//

import UIKit
import CoreData

class CandidateDetailViewController: UIViewController {
    @IBOutlet weak var firstNameLabel: UILabel!
    @IBOutlet weak var lastNameLabel: UILabel!
    @IBOutlet weak var stateLabel: UILabel!
    @IBOutlet weak var partyLabel: UILabel!
    var person:NSManagedObject!

    // modifies the labels according to the passed in person object from core data
    override func viewDidLoad() {
        super.viewDidLoad()
        self.title = "Candidate Detail"
        firstNameLabel.text = person.value(forKey: "firstName") as! String?
        lastNameLabel.text = person.value(forKey: "lastName") as! String?
        stateLabel.text = person.value(forKey: "state") as! String?
        partyLabel.text = person.value(forKey: "party") as! String?
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
}
