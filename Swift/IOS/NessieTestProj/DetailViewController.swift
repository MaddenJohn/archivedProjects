//
//  DetailViewController.swift
//  Nessie-iOS-Wrapper
//
//  Created by John Madden on 6/7/17.
//  Copyright © 2017 Nessie. All rights reserved.
//

import UIKit
import NessieFmwk

class DetailViewController: UIViewController {
    @IBOutlet weak var name: UILabel!
    @IBOutlet weak var amt: UILabel!
    @IBOutlet weak var goalName: UILabel!
    @IBOutlet weak var event: UILabel!

    var accountID:String!
    let defaults = UserDefaults.standard
    // should be 59387df1ceb8abe24251781e
    var customerID:String!
    var purchases = [MyPurchase]()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        customerID = defaults.string(forKey: "CID")
        testGetCustomer(customerId: self.customerID)
        testGetCustomerAccounts(customerId: self.customerID)
        self.accountID = defaults.string(forKey: "AID")
        testGetAllPurchasesFromAccount()

        // Do any additional setup after loading the view.
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    func testGetCustomerAccounts(customerId: String) {
        AccountRequest().getCustomerAccounts(customerId, completion:{(response, error) in
            if (error != nil) {
                print(error!)
            } else {
                if let array = response as Array<Account>? {
                    print(array)
                    let account = array[0] as Account?
                    self.accountID = (account?.accountId)!
                    self.defaults.set(self.accountID, forKey: "AID")
                    print("AID: " + self.accountID)
                    print((account?.balance)!)
                    self.amt.text = "$\((account?.balance)!)"
                }
            }
        })
    }
    
    func testGetCustomer(customerId: String) {
        CustomerRequest().getCustomer(customerId, completion:{(response, error) in
            if (error != nil) {
                print(error!)
            } else {
                if let thisCustomer = response as Customer? {
                    self.printCustomer(customer: thisCustomer)
                }
            }
        })
    }
    
    func printCustomer(customer: Customer){
        print("CID: " + customer.customerId)
        print(customer.firstName + " " + customer.lastName)
        print(customer.address.city + ", " + customer.address.state)
        print(customer.address.streetName + " " + customer.address.streetNumber)
        print(customer.address.zipCode)
        self.name.text = customer.firstName + " " + customer.lastName
    }
    
    func testGetAllPurchasesFromAccount() {
        PurchaseRequest().getPurchasesFromAccountId(self.accountID, completion:{(response, error) in
            if (error != nil) {
                print(error!)
            } else {
                if let array = response as Array<Purchase>? {
                    for purchase in array {
                        self.testGetPurchase(PurchaseId: purchase.purchaseId)
                    }
                }
            }
        })
    }
    
    func testGetPurchase(PurchaseId: String) {
        PurchaseRequest().getPurchase(PurchaseId, completion:{(response, error) in
            if (error != nil) {
                print(error!)
            } else {
                if let purchase = response as Purchase? {
                    print(purchase.amount)
                    print(purchase.description!)
                    print(purchase.purchaseDate!)
                    self.purchases.append(MyPurchase(amount: purchase.amount, description: purchase.description!, date: purchase.purchaseDate!))
                }
            }
        })
    }
    

    
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if let destinationViewController = segue.destination as? PurchasesTableViewController {
            destinationViewController.purchases = self.purchases
        }
    }
 

}
