import SwiftUI

// General list/detail adaptation, iOS 16+. No hardware/posture inference.
struct DuoArticle: Identifiable, Hashable {
    let id: String
    let title: String
    let content: String
}

@available(iOS 16.0, *)
struct DuoContentView: View {
    let articles: [DuoArticle]
    @State private var selectedID: DuoArticle.ID?

    var body: some View {
        NavigationSplitView {
            List(articles, selection: $selectedID) { article in
                NavigationLink(value: article.id) {
                    Text(article.title)
                }
            }
            .navigationTitle("Articles")
        } detail: {
            if let article = articles.first(where: { $0.id == selectedID }) {
                DuoDetailView(article: article)
            } else {
                Text("Select an article")
            }
        }
    }
}

struct DuoDetailView: View {
    let article: DuoArticle

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                Text(article.title).font(.largeTitle)
                Text(article.content)
            }
            .frame(maxWidth: .infinity, alignment: .leading)
            .padding()
        }
        .navigationTitle(article.title)
    }
}
