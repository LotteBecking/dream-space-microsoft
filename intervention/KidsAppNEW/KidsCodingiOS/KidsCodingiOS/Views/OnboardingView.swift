import SwiftUI

struct OnboardingView: View {
    @EnvironmentObject private var store: AppStore
    @Binding var isPresented: Bool

    @State private var name = ""
    @State private var age = 10

    var body: some View {
        NavigationStack {
            VStack(spacing: 20) {
                Text("Welcome to CodeQuest! 🚀")
                    .font(.largeTitle.bold())
                    .multilineTextAlignment(.center)

                Text("Let's set up your coding adventure.")
                    .foregroundStyle(.secondary)

                VStack(alignment: .leading, spacing: 12) {
                    Text("What's your name?")
                        .font(.headline)
                    TextField("Enter your name", text: $name)
                        .textFieldStyle(.roundedBorder)
                }

                VStack(alignment: .leading, spacing: 12) {
                    Text("How old are you?")
                        .font(.headline)
                    Picker("Age", selection: $age) {
                        ForEach(8...18, id: \.self) { value in
                            Text("\(value) years old").tag(value)
                        }
                    }
                    .pickerStyle(.wheel)
                    .frame(height: 120)
                }

                Button {
                    store.saveOnboarding(name: name.trimmingCharacters(in: .whitespacesAndNewlines), age: age)
                    isPresented = false
                } label: {
                    Text("Start My Journey! 🎯")
                        .frame(maxWidth: .infinity)
                }
                .buttonStyle(.borderedProminent)
                .disabled(name.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty)

                Spacer()
            }
            .padding()
            .navigationBarTitleDisplayMode(.inline)
        }
    }
}
