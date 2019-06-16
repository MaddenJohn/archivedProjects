//
//  ViewController.swift
//  maddenjonathan-hw2
//
//  Created by John Madden on 2/3/17.
//  Copyright © 2017 cs378. All rights reserved.
//

import UIKit

class ViewController: UIViewController, UITextFieldDelegate {
    // 2 textInput fields and one Laber for User Interaction
    @IBOutlet weak var inputName: UITextField!
    @IBOutlet weak var inputCity: UITextField!
    @IBOutlet weak var message: UILabel!
    
    // Function to set delegates
    override func viewDidLoad() {
        super.viewDidLoad()
        self.inputName.delegate = self
        self.inputCity.delegate = self
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
    
    // This fuction will make the keyboard disappear when return is pressed
    func textFieldShouldReturn(_ textField: UITextField) -> Bool {
        self.view.endEditing(true)
        return false
    }

    // Button handler for different user interactions
    @IBAction func btnSaveClicked(_ sender: Any) {
        if(inputName.text!.isEmpty || inputCity.text!.isEmpty) {
            message.text = "You must enter a value for *both* name and city!!"
        }
        else {
            message.text = "\(inputName.text!) - \(inputCity.text!)"
        }
    }
}
