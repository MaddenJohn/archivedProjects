//
//  RegistrationViewController.swift
//  dineTexas
//
//  Created by John Madden on 3/20/17.
//  Copyright © 2017 Hyun Joong Kim. All rights reserved.
//

import UIKit
import CoreData

class RegistrationVC: UIViewController {
    @IBOutlet weak var firstName: UITextField!
    @IBOutlet weak var lastName: UITextField!
    @IBOutlet weak var email: UITextField!
    @IBOutlet weak var password: UITextField!
    @IBOutlet weak var confPassword: UITextField!
    var alertController:UIAlertController? = nil
    let defaults = UserDefaults.standard
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        // Do any additional setup after loading the view.
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    
    @IBAction func createButtonHandler(_ sender: Any) {
        
        if (firstName.text == "" || lastName.text == "" || email.text == "" || password.text == "" ||
            confPassword.text == ""){
            displayAlert ("You must enter a value for all fields.")
        }
        else {
            if (password.text != confPassword.text){
                displayAlert ("Password and confirmed Password do not match. Try again")
            }
            else {
                defaults.set(email.text, forKey: "Email")
                defaults.set(password.text, forKey: "Password")
                defaults.set(true, forKey: "Login")
                savePerson(firstName:firstName.text!, lastName:lastName.text!, email:email.text!, password: password.text!)
                displayAlert ("Account created!")
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
    
    
    
    // Saves this person created to the core data. Much of this
    // code has been replicated from the code given in class, such as
    // the error checking for checking the managedContext.
    func savePerson(firstName: String, lastName: String, email: String, password: String) {
        
        let appDelegate = UIApplication.shared.delegate as! AppDelegate
        let managedContext = appDelegate.persistentContainer.viewContext
        
        // Create the entity we want to save
        let entity =  NSEntityDescription.entity(forEntityName: "Account", in: managedContext)
        
        let account = NSManagedObject(entity: entity!, insertInto:managedContext)
        
        // Set the attribute values
        account.setValue(firstName, forKey: "firstName")
        account.setValue(lastName, forKey: "lastName")
        account.setValue(email, forKey: "email")
        account.setValue(password, forKey: "password")
        
        // Commit the changes.
        do {
            try managedContext.save()
        } catch {
            // what to do if an error occurs?
            let nserror = error as NSError
            NSLog("Unresolved error \(nserror), \(nserror.userInfo)")
            abort()
        }
        
    }
    
    
    
    
    /*
     // MARK: - Navigation
     
     // In a storyboard-based application, you will often want to do a little preparation before navigation
     override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
     // Get the new view controller using segue.destinationViewController.
     // Pass the selected object to the new view controller.
     }
     */
    
}
