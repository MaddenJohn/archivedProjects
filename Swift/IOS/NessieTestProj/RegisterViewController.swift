//
//  RegisterViewController.swift
//  Nessie-iOS-Wrapper
//
//  Created by John Madden on 6/7/17.
//  Copyright © 2017 Nessie. All rights reserved.
//

import UIKit

class RegisterViewController: UIViewController {
    let defaults = UserDefaults.standard
    @IBOutlet weak var cid: UITextField!
    @IBOutlet weak var username: UITextField!
    @IBOutlet weak var password: UITextField!
    var alertController:UIAlertController? = nil
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    @IBAction func regHandler(_ sender: Any) {
        if (cid.text == "59387df1ceb8abe24251781e" && username.text != nil && password.text != nil){
            let aid:String = "593880c9ceb8abe242517823"
            defaults.set(username.text, forKey: "User")
            defaults.set(password.text, forKey: "Pass")
            defaults.set(cid.text, forKey: "CID")
            defaults.set(aid, forKey: "AID")
            DispatchQueue.main.async {
                self.performSegue(withIdentifier: "goDetail", sender: nil)
            }
        }
        else {
            displayAlert("Invalid credentials")
        }
    }
    
    func displayAlert (_ message: String){
        self.alertController = UIAlertController(title: message, message: "", preferredStyle: UIAlertControllerStyle.alert)
        let OKAction = UIAlertAction(title: "OK", style: UIAlertActionStyle.default) { (action:UIAlertAction) in
            print("Ok Button Pressed 1");
        }
        self.alertController!.addAction(OKAction)
        self.present(alertController!, animated: true, completion: nil)
    }

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */
    
    func textFieldShouldReturn(_ textField: UITextField) -> Bool {
        textField.resignFirstResponder()
        return true
    }
    
    override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent?) {
        self.view.endEditing(true)
    }

}
