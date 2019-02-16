import org.jetbrains.kotlin.gradle.tasks.KotlinCompile

plugins {
	application
	kotlin("jvm") version "1.3.21"
	id("org.openjfx.javafxplugin") version "0.0.7"
}

repositories {
	jcenter()
}

dependencies {
	implementation(kotlin("stdlib-jdk8"))
	implementation(kotlin("reflect"))
	implementation("org.jetbrains.kotlinx:kotlinx-coroutines-javafx:1.1.1")
	implementation("no.tornado:tornadofx:1.7.17")
}

tasks.withType<KotlinCompile> {
	kotlinOptions.jvmTarget = "1.8"
}

javafx {
	modules = listOf("javafx.controls", "javafx.fxml")
}