//
//  Withdrawal.swift
//  Nessie-iOS-Wrapper
//
//  Created by Lopez Vargas, Victor R. on 10/5/15.
//  Copyright (c) 2015 Nessie. All rights reserved.
//

import Foundation
import SwiftyJSON

open class Withdrawal: JsonParser {
    open var withdrawalId: String
    open var type: TransferType
    open var transactionDate: Date?
    open var status: TransferStatus
    open var payerId: String
    open var medium: TransactionMedium
    open var amount: Double
    open var description: String?
    
    public init(withdrawalId: String, type: TransferType, transactionDate: Date?, status: TransferStatus, medium: TransactionMedium, payerId: String, amount: Double, description: String?) {
        self.withdrawalId = withdrawalId
        self.type = type
        self.transactionDate = transactionDate
        self.status = status
        self.medium = medium
        self.payerId = payerId
        self.amount = amount
        self.description = description
    }
    
    public required init(data: JSON) {
        self.withdrawalId = data["_id"].string ?? ""
        self.type = TransferType(rawValue: data["type"].string ?? "") ?? .Unknown
        self.status = TransferStatus(rawValue: data["status"].string ?? "") ?? .Unknown
        self.transactionDate = data["transaction_date"].string?.stringToDate()
        self.medium = TransactionMedium(rawValue: data["medium"].string ?? "") ?? .Unknown
        self.payerId = data["payer_id"].string ?? ""
        self.amount = data["amount"].double ?? 0
        self.description = data["description"].string ?? ""
    }
    
}

open class WithdrawalRequest {
    fileprivate var requestType: HTTPType!
    fileprivate var accountId: String?
    fileprivate var withdrawalId: String?
    
    public init() {
        // not implemented
    }
    
    fileprivate func buildRequestUrl() -> String {
        // base URL
        var requestString = "\(baseString)/withdrawals/"
        
        // if a call uses accountId
        if let accountId = accountId {
            requestString = "\(baseString)/accounts/\(accountId)/withdrawals"
        }
        
        // if a call uses transferId
        if let withdrawalId = withdrawalId {
            requestString += "\(withdrawalId)"
        }
        
        // append apiKey
        requestString += "?key=\(NSEClient.sharedInstance.getKey())"
        
        return requestString
    }
    
    
    // MARK: API Requests
    
    // GET /accounts/{id}/withdrawals
    open func getWithdrawalsFromAccountId(_ accountId: String, completion: @escaping (_ withdrawalArray: Array<Withdrawal>?, _ error: NSError?) -> Void) {
        requestType = HTTPType.GET
        self.accountId = accountId
        
        let nseClient = NSEClient.sharedInstance
        let request = nseClient.makeRequest(buildRequestUrl(), requestType: requestType)
        
        nseClient.loadDataFromURL(request, completion: {(data, error) -> Void in
            if (error != nil) {
                completion(nil, error)
            } else {
                let json = JSON(data: data!)
                let response = BaseResponse<Withdrawal>(data: json)
                completion(response.requestArray, nil)
            }
        })
    }
    
    // GET /withdrawals/{id}
    open func getWithdrawal(_ withdrawalId: String, completion: @escaping (_ withdrawal: Withdrawal?, _ error: NSError?) -> Void) {
        requestType = HTTPType.GET
        self.withdrawalId = withdrawalId
        
        let nseClient = NSEClient.sharedInstance
        let request = nseClient.makeRequest(buildRequestUrl(), requestType: requestType)
        
        nseClient.loadDataFromURL(request, completion: {(data, error) -> Void in
            if (error != nil) {
                completion(nil, error)
            } else {
                let json = JSON(data: data!)
                let response = BaseResponse<Withdrawal>(data: json)
                completion(response.object, nil)
            }
        })
    }
    
    // POST /accounts/{id}/withdrawals
    open func postWithdrawal(_ newWithdrawal: Withdrawal, accountId: String, completion: @escaping (_ withdrawalResponse: BaseResponse<Withdrawal>?, _ error: NSError?) -> Void) {
        requestType = HTTPType.POST
        self.accountId = accountId
        
        let nseClient = NSEClient.sharedInstance
        let request = nseClient.makeRequest(buildRequestUrl(), requestType: self.requestType)
        
        // construct request body
        // required values: medium, amount
        var params: Dictionary<String, AnyObject> =
            ["medium": newWithdrawal.medium.rawValue as AnyObject,
             "amount": newWithdrawal.amount as AnyObject]
        
        // optional values
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "yyyy-dd-MM"
        if let transactionDate = newWithdrawal.transactionDate as Date? {
            let dateString = dateFormatter.string(from: transactionDate)
            params["transaction_date"] = dateString as AnyObject?
        }
        
        if let description = newWithdrawal.description {
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
                let response = BaseResponse<Withdrawal>(data: json)
                completion(response, nil)
            }
        })
    }
    
    // PUT /withdrawals/{id}
    open func putWithdrawal(_ updatedWithdrawal: Withdrawal, completion: @escaping (_ withdrawalResponse: BaseResponse<Withdrawal>?, _ error: NSError?) -> Void) {
        requestType = HTTPType.PUT
        withdrawalId = updatedWithdrawal.withdrawalId
        
        let nseClient = NSEClient.sharedInstance
        let request = nseClient.makeRequest(buildRequestUrl(), requestType: self.requestType)
        
        var params: Dictionary<String, AnyObject> =
            ["medium": updatedWithdrawal.medium.rawValue as AnyObject,
             "amount": updatedWithdrawal.amount as AnyObject]
        
        if let description = updatedWithdrawal.description {
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
                let response = BaseResponse<Withdrawal>(data: json)
                completion(response, nil)
            }
        })
    }
    
    // DELETE /withdrawals/{id}
    open func deleteWithdrawal(_ withdrawalId: String, completion: @escaping (_ withdrawalResponse: BaseResponse<Withdrawal>?, _ error: NSError?) -> Void) {
        requestType = HTTPType.DELETE
        self.withdrawalId = withdrawalId
        
        let nseClient = NSEClient.sharedInstance
        let request = nseClient.makeRequest(buildRequestUrl(), requestType: self.requestType)
        nseClient.loadDataFromURL(request, completion: {(data, error) -> Void in
            if (error != nil) {
                completion(nil, error)
            } else {
                let response = BaseResponse<Withdrawal>(requestArray: nil, object: nil, message: "Withdrawal deleted")
                completion(response, nil)
            }
        })
    }
}
