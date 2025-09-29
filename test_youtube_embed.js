const { chromium } = require('playwright');

async function testYouTubeEmbed() {
    console.log('🧪 Starting YouTube embed validation test...');
    
    const browser = await chromium.launch({ 
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    try {
        const page = await browser.newPage();
        
        // Navigate to course page
        console.log('📍 Navigating to course page...');
        await page.goto('http://localhost:5000/courses/32', { 
            waitUntil: 'networkidle',
            timeout: 30000 
        });
        
        // Check page loaded
        const title = await page.title();
        console.log(`✅ Page loaded: ${title}`);
        
        // Look for YouTube iframe
        console.log('🔍 Searching for YouTube iframe...');
        const youtubeIframes = await page.$$('iframe[src*="youtube.com/embed"]');
        console.log(`📺 Found ${youtubeIframes.length} YouTube iframe(s)`);
        
        if (youtubeIframes.length > 0) {
            for (let i = 0; i < youtubeIframes.length; i++) {
                const iframe = youtubeIframes[i];
                const src = await iframe.getAttribute('src');
                const isVisible = await iframe.isVisible();
                const boundingBox = await iframe.boundingBox();
                
                console.log(`🎯 iframe ${i + 1}:`);
                console.log(`   - src: ${src}`);
                console.log(`   - visible: ${isVisible}`);
                console.log(`   - dimensions: ${boundingBox ? `${boundingBox.width}x${boundingBox.height}` : 'not rendered'}`);
                console.log(`   - position: ${boundingBox ? `x:${boundingBox.x}, y:${boundingBox.y}` : 'not positioned'}`);
            }
        }
        
        // Check for YouTube Video URL section
        console.log('🔍 Checking YouTube Video URL section...');
        const youtubeSection = await page.$('h4:has-text("YouTube Video URL")');
        if (youtubeSection) {
            console.log('✅ Found "YouTube Video URL" section header');
            
            // Check if iframe is in this section
            const parentCard = await youtubeSection.locator('..').locator('..').locator('iframe[src*="youtube.com/embed"]');
            const iframeInSection = await parentCard.count();
            console.log(`📺 YouTube iframe in URL section: ${iframeInSection > 0 ? 'YES' : 'NO'}`);
        } else {
            console.log('❌ "YouTube Video URL" section not found');
        }
        
        // Take a screenshot for verification
        console.log('📸 Taking screenshot...');
        await page.screenshot({ 
            path: 'youtube_embed_test.png', 
            fullPage: true 
        });
        console.log('📸 Screenshot saved as youtube_embed_test.png');
        
        // Final validation
        console.log('\n🎯 VALIDATION RESULTS:');
        console.log(`✅ Page loads: YES`);
        console.log(`✅ YouTube iframe present: ${youtubeIframes.length > 0 ? 'YES' : 'NO'}`);
        console.log(`✅ YouTube iframe visible: ${youtubeIframes.length > 0 ? await youtubeIframes[0].isVisible() : 'NO'}`);
        console.log(`✅ Iframe dimensions valid: ${youtubeIframes.length > 0 && await youtubeIframes[0].boundingBox() ? 'YES' : 'NO'}`);
        
        return {
            success: youtubeIframes.length > 0,
            iframeCount: youtubeIframes.length,
            screenshotTaken: true
        };
        
    } catch (error) {
        console.error('❌ Test failed:', error.message);
        return { success: false, error: error.message };
    } finally {
        await browser.close();
    }
}

// Run the test
testYouTubeEmbed()
    .then(result => {
        console.log('\n🏁 Test completed:', result);
        process.exit(result.success ? 0 : 1);
    })
    .catch(error => {
        console.error('💥 Test crashed:', error);
        process.exit(1);
    });