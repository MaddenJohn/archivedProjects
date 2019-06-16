//
//  MyTableViewCell.swift
//  TestCustomTableViewCells
//
//  Created by John Madden on 2/13/17.
//  Copyright © 2017 cs378. All rights reserved.
//

import UIKit

class MyTableViewCell: UITableViewCell {

    @IBOutlet weak var lbl: UILabel!
    
    override func awakeFromNib() {
        super.awakeFromNib()
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)
    }
    @IBAction func btnAction(_ sender: Any) {
        
    }
}
