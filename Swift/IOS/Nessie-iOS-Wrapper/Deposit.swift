//
//  Deposit.swift
//  Nessie-iOS-Wrapper
//
//  Created by Lopez Vargas, Victor R. on 10/5/15.
//  Copyright (c) 2015 Nessie. All rights reserved.
//

import Foundation
import SwiftyJSON

public enum TransactionMedium : String {
    case Balance = "balance"
    case Rewards = "rewards"
    case Unknown
}

public enum TransactionType : String {
    case Payee = "payee"
    case Payer = "payer"
    case Unknown
}

open class Deposit: JsonParser {
    open var depositId: String
    open var status: BillStatus
    open var medium: TransactionMedium
    open var payeeId: String?
    open var amount: Int
    open var type: String
    open var transactionDate: Date?
    open var description: String?
    
    public init(depositId: String, status: BillStatus, medium: TransactionMedium, payeeId: String?, amount: Int, type: String, transactionDate: Date?, description: String?) {
        self.depositId = depositId
        self.status = status
        self.medium = medium
        self.payeeId = payeeId
        self.amount = amount
        self.type = type
        self.transactionDate = transactionDate
        self.description = description
    }
    
    public required init(data: JSON) {
        self.depositId = data["_id"].string ?? ""
        self.status = BillStatus(rawValue: data["status"].string ?? "") ?? .Unknown
        self.medium = TransactionMedium(rawValue: data["medium"].string ?? "") ?? .Unknown
        self.payeeId = data["payee_id"].string ?? ""
        self.amount = data["amount"].int ?? 0
        self.type = data["type"].string ?? ""
        self.transactionDate = data["transaction_date"].string?.stringToDate()
        self.description = data["description"].string ?? ""
        self.depositId = data["_id"].string ?? ""
    }
}

open class DepositRequest {
    fileprivate var requestType: HTTPType!
    fileprivate var accountId: String?
    fileprivate var depositId: String?
    
    public init () {}
    
    fileprivate func buildRequestUrl() -> String {
        
        var requestString = "\(baseString)/deposits/"
        if let accountId = accountId {
            requestString = "\(baseString)/accounts/\(accountId)/deposits"
        }
        
        if let depositId = depositId {
            requestString += "\(depositId)"
        }
        
        requestString += "?key=\(NSEClient.sharedInstance.getKey())"
        
        return requestString
    }
    
    // APIs
    open func getDeposit(_ depositId: String, completion: @escaping (_ deposit: Deposit?, _ error: NSError?) -> Void) {
        requestType = HTTPType.GET
        self.depositId = depositId
        
        let nseClient = NSEClient.sharedInstance
        let request = nseClient.makeRequest(buildRequestUrl(), requestType: requestType)
        nseClient.loadDataFromURL(request, completion: {(data, error) -> Void in
            if (error != nil) {
                completion(nil, error)
            } else {
                let json = JSON(data: data!)
                let response = BaseResponse<Deposit>(data: json)
                completion(response.object, nil)
            }
        })
    }
    
    open func getDepositsFromAccountId(_ accountId: String, completion: @escaping (_ depositArrays: Array<Deposit>?, _ error: NSError?) -> Void) {
        requestType = HTTPType.GET
        self.accountId = accountId
        
        let nseClient = NSEClient.sharedInstance
        let request = nseClient.makeRequest(buildRequestUrl(), requestType: requestType)
        nseClient.loadDataFromURL(request, completion: {(data, error) -> Void in
            if (error != nil) {
                completion(nil, error)
            } else {
                let json = JSON(data: data!)
                let response = BaseResponse<Deposit>(data: json)
                completion(response.requestArray, nil)
            }
        })
    }
    
    open func postDeposit(_ newDeposit: Deposit, accountId: String, completion: @escaping (_ depositResponse: BaseResponse<Deposit>?, _ error: NSError?) -> Void) {
        requestType = HTTPType.POST
        self.accountId = accountId
        let nseClient = NSEClient.sharedInstance
        let request = nseClient.makeRequest(buildRequestUrl(), requestType: self.requestType)
                
        var params: Dictionary<String, AnyObject> = ["medium": newDeposit.medium.rawValue as AnyObject,
                                                     "amount": newDeposit.amount as AnyObject]
        
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "yyyy-dd-MM"
        if let transactionDate = newDeposit.transactionDate as Date? {
            let dateString = dateFormatter.string(from: transactionDate)
            params["transaction_date"] = dateString as AnyObject?
        }
        
        if let description = newDeposit.description {
            params["description"] = description as AnyObject?
        }

        do {
            request.httpBody = try JSONSerialization.data(withJSONObject: params, options: [])
        } catch let error as NSError {
            request.httpBody = nil
            completion(nil, error)
        }
        
        nseClient.loadDataFromURL(request, completion: {(data, error) -> Void in
            if (error != nil) {
                completion(nil, error)
            } else {
                let json = JSON(data: data!)
                let response = BaseResponse<Deposit>(data: json)
                completion(response, nil)
            }
        })
    }
    
    open func putDeposit(_ updatedDeposit: Deposit, completion: @escaping (_ depositResponse: BaseResponse<Deposit>?, _ error: NSError?) -> Void) {
        requestType = HTTPType.PUT
        depositId = updatedDeposit.depositId
        let nseClient = NSEClient.sharedInstance
        let request = nseClient.makeRequest(buildRequestUrl(), requestType: self.requestType)
        
        var params: Dictionary<String, AnyObject> = ["medium": updatedDeposit.medium.rawValue as AnyObject,
                                                     "amount": updatedDeposit.amount as AnyObject]
        if let description = updatedDeposit.description {
            params["description"] = description as AnyObject?
        }
        
        do {
            request.httpBody = try JSONSerialization.data(withJSONObject: params, options: [])
        } catch let error as NSError {
            request.httpBody = nil
            completion(nil, error)
        }
        
        nseClient.loadDataFromURL(request, completion: {(data, error) -> Void in
            if (error != nil) {
                completion(nil, error)
            } else {
                let json = JSON(data: data!)
                let response = BaseResponse<Deposit>(data: json)
                completion(response, nil)
            }
        })
    }
    
    open func deleteDeposit(_ depositId: String, completion: @escaping (_ depositResponse: BaseResponse<Deposit>?, _ error: NSError?) -> Void) {
        requestType = HTTPType.DELETE
        self.depositId = depositId
        
        let nseClient = NSEClient.sharedInstance
        let request = nseClient.makeRequest(buildRequestUrl(), requestType: self.requestType)
        nseClient.loadDataFromURL(request, completion: {(data, error) -> Void in
            if (error != nil) {
                completion(nil, error)
            } else {
                let response = BaseResponse<Deposit>(requestArray: nil, object: nil, message: "Deposit deleted")
                completion(response, nil)
            }
        })
    }
}
