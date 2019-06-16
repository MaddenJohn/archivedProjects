//
//  myPageViewController.swift
//  MaddenJonathan-hw6
//
//  Created by John Madden on 2/27/17.
//  Copyright © 2017 cs378. All rights reserved.
//

import UIKit

class myPageViewController: UIPageViewController {
    
    // Initialization of the list of different view controllers based on the
    // different images
    fileprivate(set) lazy var viewControllersList: [UIViewController] = {
        return [self.newViewController(1),
                self.newViewController(2),
                self.newViewController(3),
                self.newViewController(4),
                self.newViewController(5),
                self.newViewController(6),
                self.newViewController(7)]
    }()
    
    // Function used to initialize view controllers. Sets the index variable accordingly
    fileprivate func newViewController(_ newIndex: Int) -> UIViewController {
        let result:myViewController = UIStoryboard(name: "Main", bundle: nil).instantiateViewController(withIdentifier: "viewController") as! myViewController
        result.index = newIndex
        return result;
    }
    
    // This function sets the first page as well as the colors.
    override func viewDidLoad() {
        super.viewDidLoad()
        dataSource = self
        
        if let firstViewController = viewControllersList.first {
            setViewControllers([firstViewController],
                               direction: .forward,
                               animated: true,
                               completion: nil)
        }
        let pageControl = UIPageControl.appearance()
        pageControl.pageIndicatorTintColor = UIColor.white
        pageControl.currentPageIndicatorTintColor = UIColor.green
        pageControl.backgroundColor = UIColor.lightGray
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
}

// This extension handles the changes between each of the view controllers with
// the swiping of the screen.
extension myPageViewController: UIPageViewControllerDataSource {
    
    func pageViewController(_ pageViewController: UIPageViewController,
                            viewControllerBefore viewController: UIViewController) -> UIViewController? {
        guard let viewControllerIndex = viewControllersList.index(of: viewController) else {
            return nil
        }
        
        var previousIndex = viewControllerIndex - 1
        
        if previousIndex < 0 {
            previousIndex = 6
        }
        
        return viewControllersList[previousIndex]
    }
    
    func pageViewController(_ pageViewController: UIPageViewController,
                            viewControllerAfter viewController: UIViewController) -> UIViewController? {
        guard let viewControllerIndex = viewControllersList.index(of: viewController) else {
            return nil
        }
        
        var nextIndex = viewControllerIndex + 1
        
        if nextIndex > 6 {
            nextIndex = 0
        }
        
        return viewControllersList[nextIndex]
    }
    
    func presentationCount(for pageViewController: UIPageViewController) -> Int {
        return viewControllersList.count
    }
    
    func presentationIndex(for pageViewController: UIPageViewController) -> Int {
        guard let firstViewController = viewControllers?.first,
            let firstViewControllerIndex = viewControllersList.index(of: firstViewController) else {
                return 0
        }
        
        return firstViewControllerIndex
    }
}
