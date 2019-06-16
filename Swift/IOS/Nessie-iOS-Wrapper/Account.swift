//
//  Account.swift
//  Nessie-iOS-Wrapper
//
//  Created by Lopez Vargas, Victor R. on 10/5/15.
//  Copyright (c) 2015 Nessie. All rights reserved.
//

import Foundation
import SwiftyJSON

public enum AccountType: String {
    case CreditCard = "Credit Card"
    case Savings
    case Checking
    case Unknown = ""
}

open class Account: JsonParser {
    
    open var accountId: String
    open var accountType: AccountType
    open var nickname: String
    open var rewards: Int
    open var balance: Int
    open var accountNumber: String?
    open var customerId: String
    
    public init(accountId: String, accountType: AccountType, nickname: String, rewards: Int, balance: Int, accountNumber: String?, customerId: String) {
        self.accountId = accountId
        self.accountType = accountType
        self.nickname = nickname
        self.rewards = rewards
        self.balance = balance
        self.accountNumber = accountNumber
        self.customerId = customerId
    }
    
    public required init(data: JSON) {
        self.accountId = data["_id"].string ?? ""
        self.accountType = AccountType(rawValue: data["type"].string ?? "")!
        self.nickname = data["nickname"].string ?? ""
        self.rewards = data["rewards"].int ?? 0
        self.balance = data["balance"].int ?? 0
        self.accountNumber = data["account_number"].string ?? nil
        self.customerId = data["customer_id"].string ?? ""
    }
}

open class AccountRequest {
    fileprivate var requestType: HTTPType!
    fileprivate var accountId: String?
    fileprivate var accountType: AccountType?
    fileprivate var customerId: String?
    
    public init () {}

    fileprivate func buildRequestUrl() -> String {
        
        var requestString = "\(baseString)/accounts"
        if let accountId = accountId {
            requestString += "/\(accountId)"
        }
        
        if let customerId = customerId {
            requestString = "\(baseString)/customers/\(customerId)/accounts"
        }
        
        if (self.requestType == HTTPType.POST) {
            requestString = "\(baseString)/customers/\(self.customerId!)/accounts"
        }
        
        if (self.requestType == HTTPType.GET && self.accountId == nil && self.accountType != nil) {
            var typeParam = self.accountType!.rawValue
            typeParam = typeParam.replacingOccurrences(of: " ", with: "%20")
            requestString += "?type=\(typeParam)&key=\(NSEClient.sharedInstance.getKey())"
            return requestString
        }

        requestString += "?key=\(NSEClient.sharedInstance.getKey())"
        
        return requestString
    }
    
    // APIs
    open func getAccounts(_ accountType: AccountType?, completion:@escaping (_ accountsArrays: Array<Account>?, _ error: NSError?) -> Void) {
        requestType = HTTPType.GET
        self.accountType = accountType

        let nseClient = NSEClient.sharedInstance
        let request = nseClient.makeRequest(buildRequestUrl(), requestType: requestType)
        nseClient.loadDataFromURL(request, completion: {(data, error) -> Void in
            if (error != nil) {
                completion(nil, error)
            } else {
                guard let data = data else {
                    completion(nil, genericError)
                    return
                }
                let json = JSON(data: data)
                let response = BaseResponse<Account>(data: json)
                completion(response.requestArray, nil)
            }
        })
    }

    open func getAccount(_ accountId: String, completion: @escaping (_ account:Account?, _ error: NSError?) -> Void) {
        self.requestType = HTTPType.GET
        self.accountId = accountId
        
        let nseClient = NSEClient.sharedInstance
        let request = nseClient.makeRequest(buildRequestUrl(), requestType: self.requestType)
        nseClient.loadDataFromURL(request, completion: {(data, error) -> Void in
            if (error != nil) {
                completion(nil, error)
            } else {
                let json = JSON(data: data!)
                let response = BaseResponse<Account>(data: json)
                completion(response.object, nil)
            }
        })
    }

    open func getCustomerAccounts(_ customerId: String, completion: @escaping (_ accountsArrays: Array<Account>?, _ error: NSError?) -> Void) {
        self.requestType = HTTPType.GET
        self.customerId = customerId
        
        let nseClient = NSEClient.sharedInstance
        let request = nseClient.makeRequest(buildRequestUrl(), requestType: self.requestType)
        nseClient.loadDataFromURL(request, completion: {(data, error) -> Void in
            if (error != nil) {
                completion(nil, error)
            } else {
                let json = JSON(data: data!)
                let response = BaseResponse<Account>(data: json)
                completion(response.requestArray, nil)
            }
        })
    }

    open func postAccount(_ newAccount: Account, completion: @escaping (_ accountResponse: BaseResponse<Account>?, _ error: NSError?) -> Void) {
        self.requestType = HTTPType.POST
        self.customerId = newAccount.customerId
        
        let nseClient = NSEClient.sharedInstance
        let request = nseClient.makeRequest(buildRequestUrl(), requestType: self.requestType)
        var params: Dictionary<String, AnyObject> = ["nickname": newAccount.nickname as AnyObject, "type":newAccount.accountType.rawValue as AnyObject, "balance": newAccount.balance as AnyObject, "rewards": newAccount.rewards as AnyObject]
        if let accountNumber = newAccount.accountNumber as String? {
            params["account_number"] = accountNumber as AnyObject?
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
                let response = BaseResponse<Account>(data: json)
                completion(response, nil)
            }
        })
    }

    open func putAccount(_ accountId: String, nickname: String, accountNumber: String?, completion: @escaping (_ accountResponse: BaseResponse<Account>?, _ error: NSError?) -> Void) {
        self.requestType = HTTPType.PUT
        self.accountId = accountId
        
        let nseClient = NSEClient.sharedInstance
        let request = nseClient.makeRequest(buildRequestUrl(), requestType: self.requestType)

        var params: Dictionary<String, AnyObject> = ["nickname": nickname as AnyObject]
        if let newAccountNumber = accountNumber as String? {
            params["account_number"] = newAccountNumber as AnyObject?
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
                let response = BaseResponse<Account>(data: json)
                completion(response, nil)
            }
        })
    }
    
    open func deleteAccount(_ accountId: String, completion: @escaping (_ accountResponse: BaseResponse<Account>?, _ error: NSError?) -> Void) {
        self.requestType = HTTPType.DELETE
        self.accountId = accountId
        
        let nseClient = NSEClient.sharedInstance
        let request = nseClient.makeRequest(buildRequestUrl(), requestType: self.requestType)
        nseClient.loadDataFromURL(request, completion: {(data, error) -> Void in
            if (error != nil) {
                completion(nil, error)
            } else {
                let response = BaseResponse<Account>(requestArray: nil, object: nil, message: "Account deleted")
                completion(response, nil)
            }
        })
    }
}
