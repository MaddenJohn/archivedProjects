//
//  Transfer.swift
//  Nessie-iOS-Wrapper
//
//  Created by Lopez Vargas, Victor R. on 10/5/15.
//  Copyright (c) 2015 Nessie. All rights reserved.
//

import Foundation
import SwiftyJSON

public enum TransferType: String {
    case P2P = "p2p"
    case Deposit = "deposit"
    case Withdrawal = "withdrawal"
    case Unknown
}

public enum TransferStatus: String {
    case Pending = "pending"
    case Cancelled = "cancelled"
    case Completed = "completed"
    case Unknown
}

open class Transfer: JsonParser {
    open var transferId: String
    open var type: TransferType
    open var transactionDate: Date?
    open var status: TransferStatus
    open var medium: TransactionMedium
    open var payerId: String
    open var payeeId: String
    open var amount: Double
    open var description: String?
    
    public init(transferId: String, type: TransferType, transactionDate: Date?, status: TransferStatus, medium: TransactionMedium, payerId: String, payeeId: String, amount: Double, description: String?) {
        self.transferId = transferId
        self.type = type
        self.transactionDate = transactionDate
        self.status = status
        self.medium = medium
        self.payerId = payerId
        self.payeeId = payeeId
        self.amount = amount
        self.description = description
    }
    
    public required init(data: JSON) {
        self.transferId = data["_id"].string ?? ""
        self.type = TransferType(rawValue: data["type"].string ?? "") ?? .Unknown
        self.status = TransferStatus(rawValue: data["status"].string ?? "") ?? .Unknown
        self.transactionDate = data["transaction_date"].string?.stringToDate()
        self.medium = TransactionMedium(rawValue: data["medium"].string ?? "") ?? .Unknown
        self.payerId = data["payer_id"].string ?? ""
        self.payeeId = data["payee_id"].string ?? ""
        self.amount = data["amount"].double ?? 0
        self.description = data["description"].string ?? ""
    }
    
}

open class TransferRequest {
    fileprivate var requestType: HTTPType!
    fileprivate var accountId: String?
    fileprivate var transferId: String?
    
    public init () {
        // not implemented
    }
    
    fileprivate func buildRequestUrl() -> String {
        // base URL
        var requestString = "\(baseString)/transfers/"
        
        // if a call uses accountId
        if let accountId = accountId {
            requestString = "\(baseString)/accounts/\(accountId)/transfers"
        }
        
        // if a call uses transferId
        if let transferId = transferId {
            requestString += "\(transferId)"
        }
        
        // append apiKey
        requestString += "?key=\(NSEClient.sharedInstance.getKey())"
        
        return requestString
    }
    
    fileprivate func setUp(_ reqType: HTTPType, accountId: String?, transferId: String?) {
        self.requestType = reqType
        self.accountId = accountId
        self.transferId = transferId
    }
    
    // MARK: API Requests
    
    // GET /accounts/{id}/transfers
    open func getTransfersFromAccountId(_ accountId: String, completion: @escaping (_ transferArray: Array<Transfer>?, _ error: NSError?) -> Void) {
        requestType = HTTPType.GET
        self.accountId = accountId
        
        let nseClient = NSEClient.sharedInstance
        let request = nseClient.makeRequest(buildRequestUrl(), requestType: requestType)
        
        nseClient.loadDataFromURL(request, completion: {(data, error) -> Void in
            if (error != nil) {
                completion(nil, error)
            } else {
                let json = JSON(data: data!)
                let response = BaseResponse<Transfer>(data: json)
                completion(response.requestArray, nil)
            }
        })
    }
    
    // GET /transfers/{transferId}
    open func getTransfer(_ transferId: String, completion: @escaping (_ transfer: Transfer?, _ error: NSError?) -> Void) {
        requestType = HTTPType.GET
        self.transferId = transferId
        
        let nseClient = NSEClient.sharedInstance
        let request = nseClient.makeRequest(buildRequestUrl(), requestType: requestType)
        
        nseClient.loadDataFromURL(request, completion: {(data, error) -> Void in
            if (error != nil) {
                completion(nil, error)
            } else {
                let json = JSON(data: data!)
                let response = BaseResponse<Transfer>(data: json)
                completion(response.object, nil)
            }
        })
    }
    
    // POST /accounts/{id}/transfers
    open func postTransfer(_ newTransfer: Transfer, accountId: String, completion: @escaping (_ transferResponse: BaseResponse<Transfer>?, _ error: NSError?) -> Void) {
        requestType = HTTPType.POST
        self.accountId = accountId
        
        let nseClient = NSEClient.sharedInstance
        let request = nseClient.makeRequest(buildRequestUrl(), requestType: self.requestType)
        
        // construct request body
        // required values: medium, payee_id, amount
        var params: Dictionary<String, AnyObject> =
            ["medium": newTransfer.medium.rawValue as AnyObject,
             "payee_id": newTransfer.payeeId as AnyObject,
             "amount": newTransfer.amount as AnyObject]
        
        // optional values
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "yyyy-dd-MM"
        if let transactionDate = newTransfer.transactionDate as Date? {
            let dateString = dateFormatter.string(from: transactionDate)
            params["transaction_date"] = dateString as AnyObject?
        }
        
        if let description = newTransfer.description {
            params["description"] = description as AnyObject?
        }
        
        // make request
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
                let response = BaseResponse<Transfer>(data: json)
                completion(response, nil)
            }
        })
    }
    
    // PUT /transfers/{transferId}
    open func putTransfer(_ updatedTransfer: Transfer, completion: @escaping (_ transferResponse: BaseResponse<Transfer>?, _ error: NSError?) -> Void) {
        requestType = HTTPType.PUT
        transferId = updatedTransfer.transferId
        
        let nseClient = NSEClient.sharedInstance
        let request = nseClient.makeRequest(buildRequestUrl(), requestType: self.requestType)
        
        var params: Dictionary<String, AnyObject> =
            ["medium": updatedTransfer.medium.rawValue as AnyObject,
             "payee_id": updatedTransfer.payeeId as AnyObject,
             "amount": updatedTransfer.amount as AnyObject]
        
        if let description = updatedTransfer.description {
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
                let response = BaseResponse<Transfer>(data: json)
                completion(response, nil)
            }
        })
    }
    
    // DELETE /transfers/{transferId}
    open func deleteTransfer(_ transferId: String, completion: @escaping (_ transferResponse: BaseResponse<Transfer>?, _ error: NSError?) -> Void) {
        requestType = HTTPType.DELETE
        self.transferId = transferId
        
        let nseClient = NSEClient.sharedInstance
        let request = nseClient.makeRequest(buildRequestUrl(), requestType: self.requestType)
        nseClient.loadDataFromURL(request, completion: {(data, error) -> Void in
            if (error != nil) {
                completion(nil, error)
            } else {
                let response = BaseResponse<Transfer>(requestArray: nil, object: nil, message: "Transfer deleted")
                completion(response, nil)
            }
        })
    }
    
}
