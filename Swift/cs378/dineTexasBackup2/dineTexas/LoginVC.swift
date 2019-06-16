//
//  LoginVC.swift
//  dineTexas
//
//  Created by Hyun Joong Kim on 3/20/17.
//  Copyright © 2017 Hyun Joong Kim. All rights reserved.
//

import UIKit

class LoginViewController: UIViewController {

    @IBOutlet weak var email: UITextField!
    @IBOutlet weak var password: UITextField!
    var alertController:UIAlertController? = nil
    let defaults = UserDefaults.standard
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        
        if segue.identifier == "forgotPassword"{
            let nextScene = segue.destination as? ForgotPasswordViewController
            //            navigationItem.title = nil
        }
        
    }
    override func viewDidLoad() {
        super.viewDidLoad()
        
        

        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    // Check if this is a valid user through core data
    @IBAction func loginButton(_ sender: Any) {
        if (email.text == "" || password.text == ""){
            displayAlert ("You must enter a value for all fields.")
        }
        else {
            // if valid email and password, sequeue to map
            print ("performSegue to map")
            checkInput()

        }
    }
    
    func checkInput(){
        let emailDefault:String = defaults.string(forKey: "Email")!
        let passwordDefault:String = defaults.string(forKey: "Password")!
        if(emailDefault != email.text || passwordDefault != password.text){
            displayAlert("Invalid email or password. Try again.")
            //checkInput()
        }
        else {
            DispatchQueue.main.async {
             self.performSegue(withIdentifier: "loginToMap", sender: nil)
             }
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
    }*/
 

}
