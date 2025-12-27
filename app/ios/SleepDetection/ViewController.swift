import UIKit

class ViewController: UIViewController {
    override func viewDidLoad() {
        super.viewDidLoad()
        view.backgroundColor = .white
        
        // Call Rust
        let resultPtr = rust_detect_sleep(0.15)
        let result = String(cString: resultPtr!)
        // rust_free_string(resultPtr) // If we were freeing memory
        
        let label = UILabel()
        label.text = "Core says: \(result)"
        label.textAlignment = .center
        label.frame = view.bounds
        view.addSubview(label)
    }
}
