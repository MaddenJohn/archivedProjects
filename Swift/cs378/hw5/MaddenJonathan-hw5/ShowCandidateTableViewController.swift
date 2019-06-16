//
//  ShowCandidateTableViewController.swift
//  MaddenJonathan-hw5
//
//  Created by John Madden on 2/22/17.
//  Copyright © 2017 cs378. All rights reserved.
//

import UIKit
import CoreData

class ShowCandidatesTableViewController: UITableViewController {
    var people = [NSManagedObject]()
    override func viewDidLoad() {
        super.viewDidLoad()
        self.title = "Show Candidates"
    }
    
    // This function is taken from the class code for resolving 
    // problems with the entity.
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        
        let appDelegate = UIApplication.shared.delegate as! AppDelegate
        let managedContext = appDelegate.persistentContainer.viewContext
        let fetchRequest = NSFetchRequest<NSFetchRequestResult>(entityName:"Person")
        
        var fetchedResults:[NSManagedObject]? = nil
        
        do {
            try fetchedResults = managedContext.fetch(fetchRequest) as? [NSManagedObject]
        } catch {
            // what to do if an error occurs?
            let nserror = error as NSError
            NSLog("Unresolved error \(nserror), \(nserror.userInfo)")
            abort()
        }
        
        if let results = fetchedResults {
            people = results
        } else {
            print("Could not fetch")
        }
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }

    override func numberOfSections(in tableView: UITableView) -> Int {
        return 1
    }

    // Size is based on the stored core data
    override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return people.count
    }
    
    override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "cellid", for: indexPath)

        // Configure the cell based on the core data
        let person = people[indexPath.row]
        
        let tempText:String = "\(person.value(forKey: "firstName") as! String) \(person.value(forKey: "lastName") as! String)"
        cell.textLabel!.text = tempText
        cell.detailTextLabel!.text = "\(person.value(forKey: "party") as! String)"

        return cell
    }

    // send the appropriate person object to the candidate detailed view controller
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        let indexPath: Int = (self.tableView.indexPathForSelectedRow?.row)!
        let data = people[indexPath]
        if let destinationViewController = segue.destination as? CandidateDetailViewController {
            destinationViewController.person = data
        }
    }
}
