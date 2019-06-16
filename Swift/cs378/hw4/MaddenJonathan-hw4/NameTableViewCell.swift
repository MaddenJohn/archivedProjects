//
//  NameTableViewCell.swift
//  MaddenJonathan-hw4
//
//  Created by John Madden on 2/18/17.
//  Copyright © 2017 cs378. All rights reserved.
//

import UIKit

// CustomTableViewCell for displaying the name, as well as a button
class NameTableViewCell: UITableViewCell {
    var alertController:UIAlertController? = nil
    @IBOutlet weak var lastNameLabel: UILabel!
    @IBOutlet weak var firstNameLabel: UILabel!
    var age:Int!
    var viewControllerPoiner:UIViewController!
    
    override func awakeFromNib() {
        super.awakeFromNib()
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)
    }

    // button handler, which displays the first and last name, as well as the age
    @IBAction func btnHandler(_ sender: AnyObject) {
        self.alertController = UIAlertController(title: "Person", message: "\(firstNameLabel.text!) \(lastNameLabel.text!) \(age!)", preferredStyle: UIAlertControllerStyle.alert)
        
        let OKAction = UIAlertAction(title: "OK", style: UIAlertActionStyle.default) { (action:UIAlertAction) in
            print("Ok Button Pressed 1");
        }
        self.alertController!.addAction(OKAction)
        viewControllerPoiner.present(alertController!, animated: true, completion: nil)
    }
}
