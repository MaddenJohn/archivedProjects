//
//  ViewController.swift
//  dineTexas
//
//  Created by Hyun Joong Kim on 2/27/17.
//  Copyright © 2017 Hyun Joong Kim. All rights reserved.
//

import UIKit

class LogoViewController: UIViewController {
    var LogonStatusInstance:LogonStatus = LogonStatus()
    let defaults = UserDefaults.standard
    
    @IBOutlet weak var logo: UIImageView!
    override func viewDidLoad() {
        super.viewDidLoad()
        self.logo.image = UIImage(named: "logo")
        //self.logo.image = UIImage(named: "logoBlackOnWhite.png")
        print("loaded")
        
        
        // Fade the logo into and out of view
        self.logo.alpha = 0.0
        UIView.animate(withDuration: 1.0, delay: 0.5, options: .curveLinear,
                       animations: {
                        self.logo.alpha = 1.0
        },
            completion: { finished in
                if (finished) {
                    // Working on a fade out animation
                    print ("doing fadeOut")
                    self.fadeOut()
                }
        }
        )
        
        // Do any additional setup after loading the view, typically from a nib.
    }
    
    func fadeOut() {
        UIView.animate(withDuration: 1.0, delay: 0.0, options: .curveLinear,
                       animations: {
                        self.logo.alpha = 0.0
        }
        )
    }
    
    override func viewDidAppear(_ animated: Bool) {
        let isLoggedIn = LogonStatusInstance.isAuthenticatedStatus()
//        just to check constrainst:)   
 //       let isLoggedIn = false
//        Sleep for 2 sec to show logo
        sleep(5)
        if (isLoggedIn) {
            print ("performSegue")
            DispatchQueue.main.async {
                self.performSegue(withIdentifier: "logoToApp", sender: nil)
            }
        }
        else {
            DispatchQueue.main.async {
                self.performSegue(withIdentifier: "logoToRegistration", sender: nil)
            }
        }
    }
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
}

