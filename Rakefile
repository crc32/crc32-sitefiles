# Where our Bootstrap source is installed. Can be overridden by an environment variable.
BOOTSTRAP_SOURCE = ENV['BOOTSTRAP_SOURCE'] || File.expand_path("~/git/bootstrap")

# Where to find our custom LESS file.
BOOTSTRAP_CUSTOM_LESS = '_bootstrap/less/custom.less'

def different?(path1, path2)
  require 'digest/md5'
  different = false
  if File.exist?(path1) && File.exist?(path2)
    path1_md5 = Digest::MD5.hexdigest(File.read path1)
    path2_md5 = Digest::MD5.hexdigest(File.read path2)
    (path2_md5 != path1_md5)
  else
    true
  end
end

task :bootstrap => [:bootstrap_js, :bootstrap_css, :bootstrap_fonts]

task :bootstrap_js do
  require 'uglifier'
  require 'erb'

  template = ERB.new %q{
  <!-- AUTOMATICALLY GENERATED. DO NOT EDIT. -->
  <% paths.each do |path| %>
  <script type="text/javascript" src="/js/<%= path %>"></script>
  <% end %>
  }

  paths = []
  minifier = Uglifier.new
  Dir.glob(File.join(BOOTSTRAP_SOURCE, 'js', '*.js')).each do |source|
    base = File.basename(source).sub(/^(.*)\.js$/, '\1.min.js')
    paths << base
    target = File.join('js', base)
    if different?(source, target)
      File.open(target, 'w') do |out|
        out.write minifier.compile(File.read(source))
      end
    end
  end

  File.open('_includes/bootstrap.js.html', 'w') do |f|
    f.write template.result(binding)
  end
end

task :bootstrap_css do |t|
  puts "Copying LESS files"
  Dir.glob(File.join(BOOTSTRAP_SOURCE, 'less', '*.less')).each do |source|
    target = File.join('_bootstrap/less', File.basename(source))
    cp source, target if different?(source, target)
  end
  Dir.glob(File.join(BOOTSTRAP_SOURCE, 'less/mixins', '*.less')).each do |source|
    target = File.join('_bootstrap/less/mixins', File.basename(source))
    cp source, target if different?(source, target)
  end

  puts "Compiling #{BOOTSTRAP_CUSTOM_LESS}"
  sh 'lessc', '--compress', BOOTSTRAP_CUSTOM_LESS, 'css/bootstrap.min.css'
end

task :bootstrap_fonts do |t|
	puts "Copying FONT files"
	Dir.glob(File.join(BOOTSTRAP_SOURCE, 'fonts', '*.*')).each do |source|
		target = File.join('_bootstrap/fonts', File.basename(source))
		cp source, target if different?(source, target)
	end
	Dir.glob(File.join(BOOTSTRAP_SOURCE, 'fonts', '*.*')).each do |source|
		target = File.join('fonts', File.basename(source))
		cp source, target if different?(source, target)
	end
end

task :default => :jekyll

task :jekyll => :bootstrap do
  sh 'jekyll build'
end

