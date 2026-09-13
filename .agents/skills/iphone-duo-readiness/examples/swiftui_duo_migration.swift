import SwiftUI

// =============================================================================
// ❌ BEFORE: Rigid Single-Screen SwiftUI App (NOT Duo Ready)
// =============================================================================

struct LegacyArticle: Identifiable {
    let id: String
    let title: String
    let content: String
}

struct LegacyContentView: View {
    @State private var articles = [
        LegacyArticle(id: "1", title: "iPhone Duo Unveiled", content: "Dual screen capabilities change iOS..."),
        LegacyArticle(id: "2", title: "SwiftUI Adaptation", content: "Learn how to use two panes...")
    ]
    
    var body: some View {
        // ❌ Anti-pattern 1: Forced single NavigationStack prevents two-pane view on expanded displays
        NavigationStack {
            List(articles) { article in
                NavigationLink(article.title, destination: LegacyDetailView(article: article))
            }
            .navigationTitle("Articles")
        }
    }
}

struct LegacyDetailView: View {
    let article: LegacyArticle
    
    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text(article.title)
                .font(.largeTitle)
            
            Text(article.content)
            
            Spacer()
        }
        .padding()
        // ❌ Anti-pattern 2: Hardcoded fixed frame width based on single screen iPhone (390pt)
        .frame(width: 390)
    }
}


// =============================================================================
// ✅ AFTER: iPhone Duo Ready Adaptive SwiftUI App (Duo Certified)
// =============================================================================

struct DuoArticle: Identifiable, Hashable, Codable, Transferable {
    let id: String
    let title: String
    let content: String
    
    static var transferRepresentation: some TransferRepresentation {
        CodableRepresentation(contentType: .utf8PlainText)
    }
}

struct DuoContentView: View {
    @State private var articles = [
        DuoArticle(id: "1", title: "iPhone Duo Unveiled", content: "Dual screen capabilities change iOS..."),
        DuoArticle(id: "2", title: "SwiftUI Adaptation", content: "Learn how to use two panes...")
    ]
    @State private var selectedArticle: DuoArticle?
    @Environment(\.horizontalSizeClass) private var horizontalSizeClass
    
    var body: some View {
        // ✅ 1. Use NavigationSplitView for dynamic 2-pane / 1-pane transitions
        NavigationSplitView {
            List(articles, selection: $selectedArticle) { article in
                HStack {
                    Text(article.title)
                    Spacer()
                    Image(systemName: "line.3.horizontal")
                        .foregroundColor(.gray)
                }
                .draggable(article) // ✅ 2. Enable drag-and-drop between left & right displays
                .tag(article)
            }
            .navigationTitle("Articles")
        } detail: {
            if let selectedArticle {
                DuoDetailView(article: selectedArticle)
            } else {
                ContentUnavailableView(
                    "Select an Article",
                    systemImage: "sidebar.left",
                    description: Text("Choose an item from the list to view details on the second screen.")
                )
            }
        }
        .navigationSplitViewStyle(.balanced)
    }
}

struct DuoDetailView: View {
    let article: DuoArticle
    
    var body: some View {
        GeometryReader { proxy in
            // ✅ 3. Hinge Seam Awareness: Calculate buffer margins dynamically
            let isDualScreen = proxy.size.width > 600
            let seamMargin: CGFloat = isDualScreen ? 20 : 0
            
            ScrollView {
                VStack(alignment: .leading, spacing: 20) {
                    Text(article.title)
                        .font(.largeTitle)
                        .bold()
                    
                    Divider()
                    
                    Text(article.content)
                        .font(.body)
                    
                    // ✅ 4. Scene Activation Button (Open in dedicated window)
                    Button(action: {
                        openInNewScene(articleID: article.id)
                    }) {
                        Label("Open in New Window", systemImage: "macwindow.badge.plus")
                            .font(.headline)
                            .frame(maxWidth: .infinity)
                            .padding()
                            .background(Color.blue)
                            .foregroundColor(.white)
                            .cornerRadius(12)
                    }
                }
                .padding(.horizontal, 24 + seamMargin)
                .padding(.vertical, 20)
            }
        }
    }
    
    private func openInNewScene(articleID: String) {
        let userActivity = NSUserActivity(activityType: "com.duo.article.detail")
        userActivity.userInfo = ["article_id": articleID]
        
        UIApplication.shared.requestSceneSessionActivation(
            nil,
            userActivity: userActivity,
            options: nil,
            errorHandler: nil
        )
    }
}
