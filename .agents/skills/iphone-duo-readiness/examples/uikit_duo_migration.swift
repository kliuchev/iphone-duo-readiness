import UIKit

// =============================================================================
// ❌ BEFORE: Legacy UIKit Single-Screen ViewController (NOT Duo Ready)
// =============================================================================

class LegacyMainViewController: UIViewController {
    
    override func viewDidLoad() {
        super.viewDidLoad()
        setupLegacyLayout()
    }
    
    private func setupLegacyLayout() {
        // ❌ Anti-pattern 1: Using deprecated UIScreen.main.bounds
        let screenBounds = UIScreen.main.bounds
        
        let headerView = UIView(frame: CGRect(x: 0, y: 0, width: screenBounds.width, height: 120))
        headerView.backgroundColor = .systemBlue
        view.addSubview(headerView)
        
        // ❌ Anti-pattern 2: Accessing deprecated keyWindow directly
        if let keyWin = UIApplication.shared.keyWindow {
            print("Key window bounds: \(keyWin.bounds)")
        }
    }
}


// =============================================================================
// ✅ AFTER: iPhone Duo Ready UIKit Controller & SceneDelegate (Duo Certified)
// =============================================================================

// ✅ 1. Scene-Aware Window Management in SceneDelegate
class DuoSceneDelegate: UIResponder, UIWindowSceneDelegate {

    var window: UIWindow?

    func scene(
        _ scene: UIScene,
        willConnectTo session: UISceneSession,
        options connectionOptions: UIScene.ConnectionOptions
    ) {
        guard let windowScene = (scene as? UIWindowScene) else { return }
        
        let window = UIWindow(windowScene: windowScene)
        
        // ✅ 2. Use UISplitViewController for Two-Pane Layout
        let splitVC = UISplitViewController(style: .doubleColumn)
        let masterVC = DuoMasterViewController()
        let detailVC = DuoDetailViewController()
        
        splitVC.setViewController(masterVC, for: .primary)
        splitVC.setViewController(detailVC, for: .secondary)
        splitVC.preferredDisplayMode = .oneBesideOne
        splitVC.splitBehavior = .tile
        
        window.rootViewController = splitVC
        self.window = window
        window.makeKeyAndVisible()
    }
}

// ✅ 3. Scene-Aware UIKit View Controller with Flexible Constraints
class DuoMasterViewController: UIViewController {

    override func viewDidLoad() {
        super.viewDidLoad()
        view.backgroundColor = .systemBackground
        title = "Duo Master View"
        setupAdaptiveLayout()
    }
    
    private func setupAdaptiveLayout() {
        let containerView = UIView()
        containerView.translatesAutoresizingMaskIntoConstraints = false
        containerView.backgroundColor = .secondarySystemBackground
        containerView.layer.cornerRadius = 16
        view.addSubview(containerView)
        
        // ✅ 4. Use Auto Layout Relative Anchors instead of UIScreen.main.bounds
        NSLayoutConstraint.activate([
            containerView.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor, constant: 16),
            containerView.leadingAnchor.constraint(equalTo: view.safeAreaLayoutGuide.leadingAnchor, constant: 16),
            containerView.trailingAnchor.constraint(equalTo: view.safeAreaLayoutGuide.trailingAnchor, constant: -16),
            containerView.heightAnchor.constraint(equalToConstant: 180)
        ])
    }
    
    override func viewWillTransition(to size: CGSize, with coordinator: UIViewControllerTransitionCoordinator) {
        super.viewWillTransition(to: size, with coordinator: UIViewControllerTransitionCoordinator)
        
        // ✅ 5. Gracefully handle window resize and posture transitions
        coordinator.animate(alongsideTransition: { [weak self] _ in
            guard let self = self, let scene = self.view.window?.windowScene else { return }
            let isDualDisplay = scene.screen.bounds.width > 680
            print("Transitioning layout for Dual Display mode: \(isDualDisplay)")
        }, completion: nil)
    }
}

class DuoDetailViewController: UIViewController {
    override func viewDidLoad() {
        super.viewDidLoad()
        view.backgroundColor = .systemGroupedBackground
        title = "Duo Detail View"
    }
}
