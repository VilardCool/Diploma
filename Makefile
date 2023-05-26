all: run

clean:
	rm -f src/*.class out/Main.jar

Main.jar: out/parcs.jar src/*.java
	@javac -cp out/parcs.jar src/*.java
	@jar cf out/Main.jar -C src .
	@rm -f src/*.class

run: Main.jar
	@cd out && java -cp 'parcs.jar:Main.jar' Main